from Constants import AP_CONST

class Passer:
    def __init__(self):
        self.__addressMasks = AP_CONST.collection['MASKS_FOLDER']
        self.__addressTracers = AP_CONST.collection['TRACES_FOLDER']
    @property
    def addressMasks(self):
        return self.__addressMasks
    @property
    def addressTracers(self):
        return self.__addressTracers