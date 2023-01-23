import array

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as numpy
import salesman_task as st

import salesman_task

P_CROSSOVER = 0.9
P_MUTATION = 0.4
MAX_GENERATIONS = 200
POPULATION_SIZE = 200
RANDOM_SEED = 41
random.seed(RANDOM_SEED)

def main():
    tsp = salesman_task.TravelingSalesmanProblem()
    toolbox = base.Toolbox()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", array.array, fitness=creator.FitnessMin, typecode='i')  # add param typecode='i'

    toolbox.register("randomOrder", random.sample, range(len(tsp)), len(tsp))  # оператор randomOrder
    # применяет функцию random.sample() к диапазону, соответствующему задаче коммивояжера
    # (длины, равной количеству городов n). В результате генерируется
    # случайный список индексов от 0 до n – 1.
    toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomOrder)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    def tpsDiatance(individual):
        return tsp.getTotalDistance(individual)

    toolbox.register("evaluate", tpsDiatance)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(tsp))

    hof = tools.HallOfFame(30)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", numpy.min)
    stats.register("avg", numpy.mean)
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    population, logbook = st.eaSimpleWithElitism(population, toolbox,
                                              cxpb=P_CROSSOVER,
                                              mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS,
                                              stats=stats,
                                              halloffame=hof,
                                              verbose=True)

    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    # Nevals представляет количество раз, чтобы вызвать функцию оценки в итерации

    print("Лучший индивидуум = ", hof.items[0])
    print("Optimal distance = ", tsp.getTotalDistance(hof.items[0]))

    fig, axs = plt.subplots(2)

    sns.set_style("whitegrid")
    axs[0].plot(minFitnessValues, color='red')
    axs[0].plot(meanFitnessValues, color='green')
    axs[0].set_xlabel('Поколение')
    axs[0].set_ylabel('Целевая/средняя приспособленность')
    axs[0].set_title('Зависимость целевой и средней приспособленности от поколения')
    # plt.show()

    # plot the solution:
    axs[1] = tsp.plotData(hof.items[0])
    plt.show()


if __name__ == "__main__":
    main()
