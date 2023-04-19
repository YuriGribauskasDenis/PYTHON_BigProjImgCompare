from CoordCore.DataFile import TracesFile
from pathlib import Path
from CoordCore.DataWrappers import RePoint

class TracersData:
    #SUBFOLDER_NAME = 'Particle Defect MSI'
    def __init__(self, address):
        #self.__address = Path(address) / TracersData.SUBFOLDER_NAME
        self.__address = Path(address)
        self.__files = self.genFileList()
        self.__coordMap = self.genCoordMap()
    def genFileList(self):
        return [TracesFile(child) for child in self.address.iterdir() if child.is_file()]
    def __str__(self):
        res = ''
        for f_el in self.__files:
            res += f'{f_el.getName()}\n'
        return res
    def genCoordMap(self):
        coordMap = {}
        print("\nTrace Coordinate Map Generation")
        for fi in self.__files:
            cid, _, _ = fi.decodeName()
            centr_x, centr_y = fi.getDefCooerCenter()
            if cid in coordMap:
                coordMap[cid].append(RePoint(centr_x, centr_y))
            else:
                coordMap[cid] = [RePoint(centr_x, centr_y)]
        return coordMap
    @property
    def address(self):
        return self.__address
    @property
    def files(self):
        return self.__files
    @property
    def coordMap(self):
        return self.__coordMap