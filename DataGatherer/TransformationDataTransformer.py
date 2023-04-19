from pathlib import Path
import json

class Transformer:
    def __init__(self, adr):
        if isinstance(adr, Path):
            adr = str(adr)
        self.__ident = 4
        self.__address = adr
        self.__json_obj = self.__gen_json_obj()
    def __read_csv(self):
        with open(self.__address, 'r') as f:
            data = f.read().splitlines()
            return data
    def __gen_json_obj(self):
        data = self.__read_csv()
        model_data = {}
        print("\nCorrection File Reading")
        for line in data[1:]:
            arr_line = line.split(';')
            mod_name = arr_line[0]
            cam_name = arr_line[1]
            d_clip = {
                'LEFT':int(arr_line[2]),
                'TOP':int(arr_line[3]),
                'RIGHT':int(arr_line[4]),
                'BOTTOM':int(arr_line[5])
            }
            cam_data = {cam_name : d_clip}
            if mod_name not in model_data:
                model_data[mod_name] = cam_data
            else:
                model_data[mod_name][cam_name] = d_clip

        json_object = json.dumps(model_data, indent = self.__ident)
        return json_object
    @property
    def ident(self):
        return self.__ident
    @ident.setter
    def ident(self, idn):
        self.__ident = idn
        some_dict = json.loads(self.__json_obj)
        self.__json_obj = json.dumps(some_dict, indent = self.__ident)
    @property
    def address(self):
        return self.__address
    @property
    def json_obj(self):
        return self.__json_obj
    def __str__(self):
        res = f'{self.__address}\n{self.__json_obj}'
        return res