from CoordCore.DataFile import DefmapFile
from pathlib import Path
import cv2
import numpy as np
from tqdm import tqdm
from CoordCore.DataWrappers import RePoint

class DefmapData:
    SUFFIX_NAME = '.defmap'
    def __init__(self, address):
        self.__address = Path(address)
        self.__files = self.__genFileList()
        self.__fileKeys = []
        self.__fileCoords = []
        self.__fillFileData()
    def __genFileList(self):
        return [DefmapFile(child) for child in self.address.iterdir() if child.is_file() and len(child.suffixes) == 2 and child.suffixes[-2] == DefmapData.SUFFIX_NAME ]
    def __fillFileData(self):
        print("\nMask Files Data Generation")
        for fi in tqdm(self.__files):
            cid, _, _ = fi.decodeName()
            self.__fileKeys.append(cid)
            self.__fileCoords.append(self.imgToCoord(fi.getStrElement()))
    def imgToCoord(self, defmap):
        gray = cv2.imread(defmap, cv2.IMREAD_GRAYSCALE)
        _, threshed = cv2.threshold(gray.copy(), 100, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(threshed.copy(), cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)
        def_cnt = []
        for cnt in cnts:
            coord = np.rint(np.mean(cnt, axis=0)).astype(int)
            def_cnt.append(RePoint(coord[0,0], coord[0,1]))
        return def_cnt
    def __str__(self):
        res = ''
        for f_el in self.__files:
            res += f'{f_el.getName()}\n'
        return res
    @property
    def address(self):
        return self.__address
    @property
    def files(self):
        return self.__files
    @property
    def fileKeys(self):
        return self.__fileKeys
    @property
    def fileCoords(self):
        return self.__fileCoords