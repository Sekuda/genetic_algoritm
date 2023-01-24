import array

import salesman_task
import elitism
from deap import base
from deap import creator
from deap import tools
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as numpy

P_CROSSOVER = 0.9
P_MUTATION = 0.2
MAX_GENERATIONS = 300
POPULATION_SIZE = 200
RANDOM_SEED = 41
random.seed()


def main():
    tsp = salesman_task.TravelingSalesmanProblem()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
    creator.create("Individual", array.array, fitness=creator.FitnessMin, typecode='i')

    toolbox = base.Toolbox()
    toolbox.register("randomOrder", random.sample, range(len(tsp) + tsp.carCnt - 1),
                     len(tsp) + tsp.carCnt - 1)  # оператор randomOrder
    # применяет функцию random.sample() к диапазону, соответствующему задаче коммивояжера
    # (длины, равной количеству городов n). В результате генерируется
    # случайный список индексов от 0 до n – 1.
    toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomOrder)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    def tpsDiatance(individual):
        return tsp.getMaxDistance(individual), tsp.getRouteDistance(individual)

    toolbox.register("evaluate", tpsDiatance)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / len(tsp))

    hof = tools.HallOfFame(30)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", numpy.min)
    stats.register("avg", numpy.mean)
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    population, logbook = elitism.eaSimpleWithElitism(population, toolbox,
                                                      cxpb=P_CROSSOVER,
                                                      mutpb=P_MUTATION,
                                                      ngen=MAX_GENERATIONS,
                                                      stats=stats,
                                                      halloffame=hof,
                                                      verbose=True)

    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    # Nevals представляет количество раз, чтобы вызвать функцию оценки в итерации

    print("Лучший индивидуум = ", tsp.getRouteDistance(hof.items[0]))
    print("Optimal distance = ", tsp.getMaxDistance(hof.items[0]))
    print(f'Dist:  {tsp.getTotalDistance(tsp.getRoutes(hof.items[0])[0])}, '
          f'{tsp.getTotalDistance(tsp.getRoutes(hof.items[0])[1])},'
          f' {tsp.getTotalDistance(tsp.getRoutes(hof.items[0])[2])}')
    fig, axs = plt.subplots(2)

    sns.set_style("whitegrid")
    axs[0].plot(minFitnessValues, color='red')
    axs[0].plot(meanFitnessValues, color='green')
    axs[0].set_xlabel('Поколение')
    axs[0].set_ylabel('Целевая/средняя приспособленность')
    axs[0].set_title('Зависимость целевой и средней приспособленности от поколения')
    # plt.show()

    # plot the solution:
    axs[1] = tsp.plotCarsData(hof.items[0])
    plt.show()


if __name__ == "__main__":
    main()
