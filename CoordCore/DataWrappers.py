class RePoint:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    def __add__(self, p2):
        if isinstance(p2, tuple):
            x, y = p2
            return RePoint(self.__x + x, self.__y + y)
        elif isinstance(p2, RePoint):
            x, y = p2.x, p2.y
            return RePoint(self.__x + x, self.__y + y)
        else:
            raise TypeError("That data type is not supported")
    def __radd__(self, p2):
        return self + p2
    def __iadd__(self, p2):
        if isinstance(p2, tuple):
            x, y = p2
            self.__x += x
            self.__y += y
            return self
        elif isinstance(p2, RePoint):
            self.__x += p2.x
            self.__y += p2.y
            return self
        else:
            raise TypeError("That data type is not supported")
    def __truediv__(self, n):
        if isinstance(n, int) or isinstance(n, float):
            x = self.__x / n
            y = self.__y / n
            return RePoint(x,y)
        else:
            raise TypeError(f"{n} data type is not supported")
    def __itruediv__(self, n):
        if isinstance(n, int) or isinstance(n, float):
            self.__x /= n
            self.__y /= n
            return self
        else:
            raise TypeError(f"{n} data type is not supported")
    def squareDistanceFromPoint(self, p2):
        if not isinstance(p2, RePoint):
            raise ValueError(f'Argument passed "{type(p2)}" must be RePoint')
        x1, y1 = self.__x, self.__y
        x2, y2 = p2
        return (x1 - x2)**2 + (y1 - y2)**2
    def distanceFromPoint(self, p2):
        if not isinstance(p2, RePoint):
            raise ValueError(f'Argument passed "{type(p2)}" must be RePoint')
        return (self.squareDistanceFromPoint(p2))**0.5
    def __getitem__(self, i):
        if i == 0:
            return self.__x
        elif i == 1:
            return self.__y
        else:
            raise ValueError(f'index {i}" must be 0 or 1')
    def __iter__(self):
        return iter((self.__x, self.__y))
    def __str__(self):
        return f'({int(self.__x):5d}, {int(self.__y):5d})'
class ReExperiment:
    def __init__(self, p1, p2, d):
        self.__point1 = p1
        self.__point2 = p2
        self.__distance = d
        self.__detectionResult = None
    def setLocalMiss(self):
        self.__detectionResult = False
    def setLocalDetection(self):
        self.__detectionResult = True
    @property
    def detectionResult(self):
        return self.__detectionResult
    def __str__(self):
        det_res = 'DTCT' if self.__detectionResult else 'MISS'
        if self.__detectionResult is None:
            det_res = self.__detectionResult
        return f'| {self.__point1} | {self.__point2} | {self.__distance:8.2f} | {det_res} |'
class ReCase:
    def __init__(self, cid, cooedsMaskList, cooedsTraceList):
        self.__cid = cid
        self.__cooedsMaskList = cooedsMaskList
        self.__cooedsTraceList = cooedsTraceList
        self.__experiments = []
    def addEcperiment(self, reportExperiment):
        self.__experiments.append(reportExperiment)
    def __str__(self):
        s = ''
        s += f'\n{"*"*26}\nCID {self.__cid}\n'
        s += '---masks---\n'
        for mask in self.__cooedsMaskList:
            s += f'{str(mask)} '
        s += '\n---vs---\n'
        s += '--tracers--\n'
        for trace in self.__cooedsTraceList:
            s += f'{str(trace)} '
        s += f'\n{"-" * 53}\n'
        for reportE in self.__experiments:
            s += f'{str(reportE)}\n'
        s += f'{"-" * 53}\n'
        s += f'{"*"*26}\n'
        return s