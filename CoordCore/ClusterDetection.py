from itertools import combinations
from CoordCore.DataWrappers import RePoint

class Clusterer:
    def __init__(self, points, threshold):
        self.__points = points
        self.__threshold = threshold
        self.__size = len(self.__points)
        self.__prox = self.__getProximityMatrix()
        self.__clusters = self.__findClusters()
        self.__averagePoints = self.__averagePoints()

    def __squaredDistance(self, p1, p2):
        return p1.squareDistanceFromPoint(p2)

    def __getProximityMatrix(self):
        t2 = self.__threshold**2
        prox = [[False]*self.__size for k in range(self.__size)]
        for i, j in combinations(range(self.__size), 2):
            prox[j][i] = prox[i][j] = (self.__squaredDistance(self.__points[i], self.__points[j]) < t2)
        return prox

    def __findClusters(self):
        point_in_list = [None] * self.__size
        clusters = []
        for i in range(0, self.__size):
            for j in range(i + 1, self.__size):
                if self.__prox[i][j]:
                    list1 = point_in_list[i]
                    list2 = point_in_list[j]
                    if list1 is not None:
                        if list2 is None:
                            list1.append(j)
                            point_in_list[j] = list1
                        elif list2 is not list1:
                            list1 += list2
                            point_in_list[j] = list1
                            del clusters[clusters.index(list2)]
                        else:
                            pass
                    elif list2 is not None:
                        list2.append(i)
                        point_in_list[i] = list2
                    else:
                        list_new = [i, j]
                        for index in [i, j]:
                            point_in_list[index] = list_new
                        clusters.append(list_new)
            if point_in_list[i] is None:
                list_new = [i]
                point_in_list[i] = list_new
                clusters.append(list_new)
        return clusters

    def __averagePoints(self):
        newpoints = []
        for cluster in self.__clusters:
            n = len(cluster)
            p = RePoint(0,0)
            for index in cluster:
                p += self.__points[index]
            p /= n
            newpoints.append(p)
        return newpoints

    def simplify(self):
        return self.__clusters, self.__averagePoints