from pathlib import Path
from Constants import NP_CONST

class DataFile:
    def __init__(self, pathElement):
        self.__pathElement = Path(pathElement)
    def getPathElement(self):
        return self.__pathElement
    def getStrElement(self):
        return self.__pathElement.__str__()
    def getName(self):
        return  self.__pathElement.name.split('.')[0]

class DefmapFile(DataFile):
    def __decodeName(self):
        # FULL_FUSED_MSI_IMAGE_[20220830][161703][390749][LWB][FROZEN WHITE][CAMERA1103]
        everything = self.getName().split('[')
        cid = everything[3][:-1]
        model = everything[4][:-1]
        cam = everything[6][6:-1]
        return int(cid), model, int(cam)
    def decodeName(self):
        cid, model, cam = self.__decodeName()
        return cid, model, cam

class TracesFile(DataFile):
    def __decodeName(self):
        # [20220830][161703][390749][LWB][FROZEN WHITE][CAMERA11103][99][x13193][y02925]
        everything = self.getName().split('[')
        cid = int(everything[3][:-1])
        model = everything[4][:-1]
        cam = int(everything[6][7:-1])
        centr_x = int(everything[8][1:-1])
        centr_y = int(everything[9][1:-1])
        return cid, model, cam, centr_x, centr_y
    def decodeName(self):
        cid, model, cam, _, _ = self.__decodeName()
        return cid, model, cam
    def getDefCooerCenter(self):
        _, _, _, centr_x, centr_y = self.__decodeName()
        return centr_x, centr_y