from CoordCore.CompareMsi import Comparer
from DataGatherer.ConstantsPasser import Passer

pss = Passer()
folderM = pss.addressMasks
folderT = pss.addressTracers

comparer = Comparer(folderM, folderT)
comparer.compare()