import json
from pathlib import Path
from DataGatherer.TransformationDataTransformer import Transformer
from DataGatherer.TransformationDataSaver import Saver

class Reader:
    def __init__(self, adr):
        if isinstance(adr, Path):
            adr = str(adr)
        self.__address = adr
        self.__dictionary = self.__gen_dictionary()
    def __gen_dictionary(self):
        if self.__address[-4:].lower() == 'json':
            return self.__gen_dictionary_json()
        elif self.__address[-3:].lower() == 'csv':
            return self.__gen_dictionary_trans()
        else:
            raise ValueError('provide proper address')
    def __gen_dictionary_json(self):
        with open(self.__address) as json_file:
            data = json.load(json_file)
        return data
    def __gen_dictionary_trans(self):
        t = Transformer(self.__address)
        t.ident = 4
        adr2 = Path(self.__address).resolve().parent / 'corrections_v2.json'
        s = Saver(t, str(adr2))
        s.save_dict_to_json()
        return json.loads(t.json_obj)
    @property
    def dictionary(self):
        return self.__dictionary