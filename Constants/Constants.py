from pathlib import Path
from DataGatherer.Parameters import NumericalParameters as NP
from DataGatherer.Parameters import AddressParameters as AP
from DataGatherer.Parameters import ReportParameters as RP
from DataGatherer.TransformationDataReader import Reader
from Stuff.GenerateStuff import get_folder_adr

address_constants = get_folder_adr(__file__) / 'constants.json'

NP_CONST = NP(address_constants)
AP_CONST = AP(address_constants)
RP_CONST = RP(address_constants)

TRANS_DICT_CONST = Reader(AP_CONST.collection['TRANSFORMATION_FILE']).dictionary