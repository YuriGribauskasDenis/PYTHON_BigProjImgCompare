from abc import ABC, abstractclassmethod

class Rep(ABC):
    def __init__(self, text):
        self._text = text
    @abstractclassmethod
    def genName(self):
        pass
    @abstractclassmethod
    def sendFlow(self):
        pass

class TRep(Rep):
    __adrKey = 'T'
    def sendFlow(self):
        print(f'{self.genName()}, {self._Rep__text}')
    def genName(self):
        return TRep.__adrKey * 2

class PRep(Rep):
    __adrKey = 'P'
    def sendFlow(self):
        print(f'{self.genName()}, {self._Rep__text}')
    def genName(self):
        return PRep.__adrKey * 3

def getInput(c):
    reps = {
        't' : TRep,
        'p' : PRep,
    }
    if not isinstance(c, str):
        raise TypeError(f'{c} must be string')
    csmall = c.lower()
    if not csmall in reps:
        raise ValueError(f'{c} must be from {reps.keys()}')
    return reps[csmall]

# tr = TRep("it's a trep")
# tr.sendFlow()

# pr = PRep("prep, prep, prep")
# pr.sendFlow()

rr = getInput('T')('hello, man')
rr.sendFlow()