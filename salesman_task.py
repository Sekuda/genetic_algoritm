import geopy.distance
import matplotlib.pyplot as plt
from deap import tools
from deap import algorithms
import numpy as np
import random

class TravelingSalesmanProblem:
    def __init__(self):

        # initialize instance variables:
        self.locations = list()
        self.distances = list()
        self.matrix = list()
        # initialize the data:
        self.__create_data()
        self.garageIndex = 10
        self.carCnt = 2

    def __len__(self):
        return len(self.locations)

    def __create_data(self):

        # self.locations = (("работа", 55.777780, 37.504985, 0),
        #                   ("дом", 55.738344, 37.432760, 1),
        #                   ("Глеб", 55.767825, 37.557577, 2),
        #                   ("Николета", 55.766669, 37.735562, 3),
        #                   ("Авиапарк", 55.789599, 37.531579, 4),
        #                   ("ТРЦ_Кунцево", 55.738613, 37.410496, 5),
        #                   ("ТРЦ_Хорошо", 55.777067, 37.523639, 6),
        #                   ("Леруа_Строгино", 55.811217, 37.386328, 7),
        #                   ("Алена_Работа", 55.795922, 37.297073, 8),
        #                   ("мама", 57.689495, 39.764523, 9),
        #                   ("папа", 57.613051, 39.941290, 10),
        #                   ("дача", 57.486358, 39.884197, 11),
        #                   ("г.Владимир", 56.123534, 40.392854, 12),
        #                   ("Иваново", 56.997419, 40.974276, 13),
        #                   ("Кострома", 57.780252, 40.947147, 14),
        #                   ("Тверь", 56.852044, 35.910716, 15),
        #                   ("Переславль", 56.740552, 38.850907, 16)
        #                   )
        self.locations = (("работа", 55.713385, 37.385308, 0),
                          ("дом", 55.754132, 37.618802, 1),
                          ("Глеб", 55.728331, 37.094043, 2),
                          ("Николета", 55.819237, 37.163851, 3),
                          ("Авиапарк", 55.863934, 37.375680, 4),
                          ("ТРЦ_Кунцево", 55.815171, 37.620005, 5),
                          ("ТРЦ_Хорошо", 55.853780, 37.711477, 6),
                          ("Леруа_Строгино", 55.887616, 37.845074, 7),
                          ("Алена_Работа", 55.865288, 38.009964, 8),
                          ("мама", 55.815171, 37.995521, 9),
                          ("папа", 55.739196, 37.778877, 10),
                          ("дача", 55.702512, 37.918492, 11),
                          ("г.Владимир", 55.655588, 37.966635, 12),
                          ("Иваново", 55.615420, 37.736752, 13),
                          ("Кострома", 55.661712, 37.610377, 14),
                          ("Тверь", 55.707270, 37.539366, 15),
                          ("Переславль", 55.756847, 37.526127, 16)
                          )
        for i in range(len(self.locations)):
            pointA = self.locations[i]
            dy = list()
            for k in range(len(self.locations)):
                pointB = self.locations[k]
                distance = geopy.distance.geodesic(pointA[1:3], pointB[1:3]).km
                self.distances.append((pointA[3], pointB[3], distance))
                dy.append(distance)
            self.matrix.append(dy)

    def getTotalDistance(self, indices):
        total_distance = 0
        for i in range(len(indices)):
            k = i + 1
            if k > len(indices) - 1:
                k = 0
            total_distance += self.matrix[indices[i]][indices[k]]
        return total_distance

    def getRoutes(self, indices):
        car_distances = []
        cityValues = [x[3] for x in self.locations]  # it is city
        carValues = [x for x in indices if x not in cityValues]
        carInd = [indices.index(x) for x in carValues]
        carInd.insert(0, 0)
        carInd.append(len(indices))

        for x in range(len(carInd) - 1):
            distance = indices[carInd[x]:carInd[x + 1]]
            distance = [x for x in distance if (x not in carValues and x != self.garageIndex)]
            distance.insert(0, self.garageIndex)
            distance.append(self.garageIndex)
            car_distances.append(distance)
        return car_distances

    def getRouteDistance(self, indices):
        car_distances = self.getRoutes(indices)
        routeDistance = 0
        for distance in car_distances:
            distance = self.getTotalDistance(distance)
            routeDistance += distance
        return routeDistance

    def getMaxDistance(self, indices):
        car_distances = self.getRoutes(indices)
        maxCarDistance = 0
        for distance in car_distances:
            distance = self.getTotalDistance(distance)
            maxCarDistance = max(maxCarDistance, distance)
        return maxCarDistance

    def plotData(self, indices):

        # plot the dots representing the cities:
        # plt.scatter(*zip(*self.locations), marker='.', color='red')
        plt.scatter(*zip(*[(x[2], x[1]) for x in self.locations]), marker='.', color='red')

        # create a list of the corresponding city locations:
        locs = [(self.locations[i][2], self.locations[i][1]) for i in indices]
        locs.append(locs[0])

        # plot a line between each pair of consequtive cities:
        plt.plot(*zip(*locs), linestyle='-', color='blue')

        # Loop for annotation of all points
        for i in range(len(self.locations)):
            plt.annotate(self.locations[i][0], (self.locations[i][2], self.locations[i][1] + 0.001))

        return plt

    def plotCarsData(self, indices):
        carsDistances = self.getRoutes(indices)
        # plot the dots representing the cities:
        # plt.scatter(*zip(*self.locations), marker='.', color='red')
        plt.scatter(*zip(*[(x[2], x[1]) for x in self.locations]), marker='.', color='red')

        color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(self.carCnt)]
        i = 0
        for distance in carsDistances:
            # create a list of the corresponding city locations:
            locs = [(self.locations[i][2], self.locations[i][1]) for i in distance]
            locs.append(locs[0])

            # plot a line between each pair of consequtive cities:
            plt.plot(*zip(*locs), linestyle='-', color=color[i])
            i += 1

        # Loop for annotation of all points
        for i in range(len(self.locations)):
            plt.annotate(self.locations[i][0], (self.locations[i][2], self.locations[i][1] + 0.001))

        return plt


# testing the class:
def main():
    # create a problem instance:
    tsp = TravelingSalesmanProblem()

    # optimalSolution = [8, 1, 2, 3, 4, 5, 6, 7, 0, 9, 10, 11, 12, 13, 14, 15, 16]
    #
    # print("Optimal solution = ", optimalSolution)
    # print("Optimal distance = ", tsp.getTotalDistance(optimalSolution))
    # # plot the solution:
    # plot = tsp.plotData(optimalSolution)
    # plot.show()

    optimalSolution2 = [8, 1, 2, 3, 4, 5, 21, 6, 7, 0, 9, 10, 11, 12, 22, 13, 14, 15, 16]
    print("Max car distance = ", tsp.getMaxDistance(optimalSolution2))

    plot = tsp.plotCarsData(optimalSolution2)
    plot.show()


if __name__ == "__main__":
    main()
