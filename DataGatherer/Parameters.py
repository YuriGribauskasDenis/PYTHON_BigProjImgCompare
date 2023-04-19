import json

class Parameters:
    def __init__(self):
        self.__collection = {}
        self.__keyword = ''
    @property
    def keyword(self):
        return self.__keyword
    @property
    def collection(self):
        return self.__collection
    def __str__(self):
        res = 'Parameter object:\n'
        for key, value in self.__collection.items():
            res += f'{key} : {value}\n'
        return res
    def __set_attributes_from_dict(self, new_attributes):
        for k, v in new_attributes.items():
            k = k.upper()
            if k in self.__collection:
                self.__collection[k] = v
    def __load_json_config(self, path):
        params = json.load(open(path, 'r'))[self.__keyword]
        self.__set_attributes_from_dict(params)
    def __init_data(self, adr):
        self.__load_json_config(adr)
class AddressParameters(Parameters):
    def __init__(self, adr):
        super().__init__()
        self._Parameters__collection['MASKS_FOLDER'] = None
        self._Parameters__collection['TRACES_FOLDER'] = None
        self._Parameters__collection['TRANSFORMATION_FILE'] = None
        self._Parameters__keyword = 'input_addresses'
        self._Parameters__init_data(adr)
class NumericalParameters(Parameters):
    def __init__(self, adr):
        super().__init__()
        self._Parameters__collection['CAPTURE_DISTANCE'] = None
        self._Parameters__collection['CLONE_DISTANCE'] = None
        self._Parameters__keyword = 'numerical_constances'
        self._Parameters__init_data(adr)
        self.__numerize_data()
    def __numerize_data(self):
        F_C_JSON = ','
        F_C_Pyth = '.'
        for k, v in self._Parameters__collection.items():
            if F_C_JSON in v:
                self._Parameters__collection[k] = float(v.replace(F_C_JSON, F_C_Pyth))
            else:
                self._Parameters__collection[k] = int(v)
class ReportParameters(Parameters):
    def __init__(self, adr):
        super().__init__()
        self._Parameters__collection['OUTPUT_TYPE'] = None
        self._Parameters__keyword = 'report_constants'
        self._Parameters__init_data(adr)
        self.__upper_data()
    def __upper_data(self):
        for k, v in self._Parameters__collection.items():
            self._Parameters__collection[k] = v.upper()