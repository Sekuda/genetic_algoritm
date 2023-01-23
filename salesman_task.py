import geopy.distance
import matplotlib.pyplot as plt
from deap import tools
from deap import algorithms

class TravelingSalesmanProblem:
    def __init__(self):

        # initialize instance variables:
        self.locations = list()
        self.distances = list()
        self.matrix = list()
        # initialize the data:
        self.__create_data()

    def __len__(self):
        return len(self.locations)

    def getTotalDistance(self, indices):
        total_distance = 0
        for i in range(len(indices)):
            k = i + 1
            if k > len(indices)-1:
                k = 0
            total_distance += self.matrix[indices[i]][indices[k]]
        return total_distance,

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

    def __create_data(self):

        self.locations = (("работа", 55.777780, 37.504985, 0),
                          ("дом", 55.738344, 37.432760, 1),
                          ("Глеб", 55.767825, 37.557577, 2),
                          ("Николета", 55.766669, 37.735562, 3),
                          ("Авиапарк", 55.789599, 37.531579, 4),
                          ("ТРЦ_Кунцево", 55.738613, 37.410496, 5),
                          ("ТРЦ_Хорошо", 55.777067, 37.523639, 6),
                          ("Леруа_Строгино", 55.811217, 37.386328, 7),
                          ("Алена_Работа", 55.795922, 37.297073, 8),
                          ("мама", 57.689495, 39.764523, 9),
                          ("папа", 57.613051, 39.941290, 10),
                          ("дача", 57.486358, 39.884197, 11),
                          ("г.Владимир", 56.123534, 40.392854, 12),
                          ("Иваново", 56.997419, 40.974276, 13),
                          ("Кострома", 57.780252, 40.947147, 14),
                          ("Тверь", 56.852044, 35.910716, 15),
                          ("Переславль", 56.740552, 38.850907, 16)
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


def eaSimpleWithElitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(halloffame.items)

        # Update the hall of fame with the generated individuals
        halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook



# testing the class:
def main():
    # create a problem instance:
    tsp = TravelingSalesmanProblem()

    optimalSolution = [8, 1, 2, 3, 4, 5, 6, 7, 0, 9, 10, 11, 12, 13, 14, 15, 16]

    print("Optimal solution = ", optimalSolution)
    print("Optimal distance = ", tsp.getTotalDistance(optimalSolution))

    # plot the solution:
    plot = tsp.plotData(optimalSolution)
    plot.show()


if __name__ == "__main__":
    main()
