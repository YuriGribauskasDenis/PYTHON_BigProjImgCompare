import json
from pathlib import Path
from DataGatherer.TransformationDataTransformer import Transformer

class Saver:
    def __init__(self, data, adr = 4):
        self.__transformer_data = data
        self.__address = adr
    def save_dict_to_json(self):
        if isinstance(self.__address, Path):
            output_address = str(self.__address)
        else:
            output_address = self.__address
        with open(output_address, "w") as outfile:
            outfile.write(self.__transformer_data.json_obj)