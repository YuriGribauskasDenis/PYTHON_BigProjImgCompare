from Constants import TRANS_DICT_CONST
 
class Shifter:
    __CONVERT_TABLE = TRANS_DICT_CONST
    __BB = ["LEFT", "TOP", "RIGHT","BOTTOM"]
    def __new__(cls, *args, **kwargs):
        raise TypeError(f"Can't create {cls.__name__!r} objects directly")
    @classmethod
    def get_corrections(cls, model, camera_num):
        camera = f'CAMERA{camera_num}'
        left = cls.__CONVERT_TABLE[model][camera][cls.__BB[0]]
        top = cls.__CONVERT_TABLE[model][camera][cls.__BB[1]]
        right = cls.__CONVERT_TABLE[model][camera][cls.__BB[2]]
        bottom = cls.__CONVERT_TABLE[model][camera][cls.__BB[3]]
        return left, top, right, bottom