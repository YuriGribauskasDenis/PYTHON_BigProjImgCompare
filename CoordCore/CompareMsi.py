from CoordCore.CoordFromPSD import DefmapData
from CoordCore.CoordsFromTracers import TracersData
from CoordCore.CoordShifter import Shifter
from Constants import NP_CONST, RP_CONST
from CoordCore.NewasPaper import Report, PDFReporter, TXTReporter, callReporter
from CoordCore.ClusterDetection import Clusterer
from CoordCore.DataWrappers import ReCase, ReExperiment, RePoint

class Comparer:
    """A simple class that compares"""
    __MERGE_DISTANCE = NP_CONST.collection['CLONE_DISTANCE']
    __DETECT_DISTANCE = NP_CONST.collection['CAPTURE_DISTANCE']
    def __init__(self, defmap_adr, tracemap_adr):
        self.__defmap = DefmapData(defmap_adr)
        self.__tracemap = TracersData(tracemap_adr)
        self.__presencePseudoMap = self.__genPresenceList()
        self.__defCooedsShifted = self.__genShiftedCoordList()
        self.__coordsSimplifiedMap = self.__calcNoneOverlapList()
    def __genPresenceList(self):
        presencePseudoMap = []
        for key in self.__defmap.fileKeys:
            if key in self.__tracemap.coordMap:
                presencePseudoMap.append(True)
            else:
                presencePseudoMap.append(False)
        return presencePseudoMap
    def __genShiftedCoordList(self):
        defCooedsShifted = []
        print("\nMask Coordinates Shifting")
        for idx, check in enumerate(self.__presencePseudoMap):
            idx_element = [] # shifted element
            # SVAE LOGIC
            #=======================================
            # if not self.__presencePseudoMap[idx]:
            #     defCooedsShifted.append(idx_element)
            #     continue
            #=======================================
            for p in self.__defmap.fileCoords[idx]:
                _, model, camera_num = self.__defmap.files[idx].decodeName()
                left, top, _, _ = Shifter.get_corrections(model, camera_num)
                p += left, top
                idx_element.append(p)
            defCooedsShifted.append(idx_element)
        return defCooedsShifted
    def __calcDistanceOverlap(self, overlap_check_list):
        together_coords = [coords for sublist in overlap_check_list for coords in sublist]
        if len(together_coords) < 2:
            return together_coords
        c = Clusterer(together_coords, Comparer.__MERGE_DISTANCE)
        _, new_together_coords = c.simplify()
        return new_together_coords
    def __calcNoneOverlapList(self):
        coordsSimplifiedMap = {}
        left = 0
        n = len(self.__defmap.fileKeys)
        #overlap_check = []
        for right in range(1, n):
            cid_prev = self.__defmap.fileKeys[right - 1]
            cid_curr = self.__defmap.fileKeys[right]
            if cid_prev != cid_curr:
                # SVAE LOGIC
                #==========================================
                # if self.__presencePseudoMap[left]:
                res_lil = self.__calcDistanceOverlap(self.__defCooedsShifted[left:right])
                coordsSimplifiedMap[cid_prev] = res_lil
                #==========================================
                left = right
        # SVAE LOGIC
        #==========================================
        # if self.__presencePseudoMap[left]:
        res_lil = self.__calcDistanceOverlap(self.__defCooedsShifted[left:])
        coordsSimplifiedMap[cid_prev] = res_lil
        #==========================================
        # for k,v in coordsSimplifiedMap.items():
        #     print(k)
        #     print(v)
        return coordsSimplifiedMap
    def __evalInputArgs(self):
        together_files = len(self.__presencePseudoMap)
        true_work_files = sum(self.__presencePseudoMap)
        inspections = len(self.__coordsSimplifiedMap)
        together_coordeinates = sum([len(el) for el in self.__coordsSimplifiedMap.values()])
        return true_work_files, together_files, inspections, together_coordeinates
    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x1 - x2)**2 + (y1 - y2)**2)**(0.5)
    def __detection_dist_check(self, x1, y1, x2, y2):
        return Comparer.distance(x1, y1, x2, y2) < Comparer.__DETECT_DISTANCE
    @property
    def presencePseudoMap(self):
        return self.__presencePseudoMap
    @property
    def defmap(self):
        return self.__defmap
    @property
    def tracemap(self):
        return self.__tracemap
    def __compareHelper(self, x1, y1, x2, y2):
        d = Comparer.distance(x1, y1, x2, y2)
        rexp = ReExperiment(RePoint(x1, y1), RePoint(x2, y2), d)
        if d > Comparer.__DETECT_DISTANCE:
            rexp.setLocalMiss()
        else:
            rexp.setLocalDetection()
        return rexp
    def compare(self):
        progress = []
        dtct = 0
        miss = 0
        print("\nComparing Naive Runner")
        for key, coords in self.__coordsSimplifiedMap.items():
            if key not in self.__tracemap.coordMap:
                continue
            rc = ReCase(key, coords, self.__tracemap.coordMap[key])
            for x1, y1 in coords:
                for x2, y2 in self.__tracemap.coordMap[key]:
                    rexp = self.__compareHelper(x1, y1, x2, y2)
                    if rexp.detectionResult:
                        dtct += 1
                        flag_det = True
                        rc.addEcperiment(rexp)
                        break
                    rc.addEcperiment(rexp)
                if not rexp.detectionResult:
                    miss += 1
                progress.append(rc)
        results = dtct, miss, *self.__evalInputArgs()
        self.__initiate_report(progress, results)

    def __initiate_report(self, progress, results):
        participants_numbers = [i for i, x in enumerate(self.__presencePseudoMap) if x]
        participants_names = [self.__defmap.files[num].getName() for num in participants_numbers]
        none_participants_numbers = [i for i, x in enumerate(self.__presencePseudoMap) if not x]
        # cid-model-camera ?
        # self.__defmap.files[9].decodeName()
        # tup = self.__defmap.files[9].decodeName()
        # '-'.join(tup)
        # '-'.join(self.__defmap.files[9].decodeName())
        # none_participants_names = ['-'.join(self.__defmap.files[num].decodeName()) for num in none_participants_numbers]
        none_participants_names = [self.__defmap.files[num].getName() for num in none_participants_numbers]
        r = Report(self.__defmap.address, self.__tracemap.address)
        r.load_participants(participants_names, none_participants_names)
        r.load_progress(progress)
        r.load_results(results)
        self.__print_report(r)
    def __print_report(self, report):
        rr = callReporter(RP_CONST.collection['OUTPUT_TYPE'])(report)
        # rr = PDFReporter(report)
        # rr = TXTReporter(report)
        rr.create_report()