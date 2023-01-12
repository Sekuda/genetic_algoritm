from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as numpy

# константы задачи
ONE_MAX_LENGTH = 20  # длина индивидуума
MAX_GENERATIONS = 50  # максимальное количество поколений
HALL_OF_FAME_SIZE = 10  # количество членов зала славы
POPULATION_SIZE = 100  # количество индивидуумов в популяции
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.2  # вероятность мутации индивидуума
INDPB = 1.0 / ONE_MAX_LENGTH  # вероятность применения мутации к каждому гену

RANDOM_SEED = 41
random.seed(RANDOM_SEED)

items = (
    ("map", 9, 150), ("compass", 13, 35), ("water", 153, 200), ("sandwich", 50, 160),
    ("glucose", 15, 60), ("tin", 68, 45), ("banana", 27, 60), ("apple", 39, 40),
    ("cheese", 23, 30), ("beer", 52, 10), ("suntan cream", 11, 70), ("camera", 32, 30),
    ("t-shirt", 24, 15), ("trousers", 48, 10), ("umbrella", 73, 40), ("book", 30, 10),
    ("note-case", 22, 80), ("sunglasses", 7, 20), ("towel", 18, 12), ("socks", 4, 50),
    ("waterproof trousers", 42, 70), ("waterproof overclothes", 43, 75)
)
empty = ("empty", 0, 0)


def getEmpty():
    return empty


toolbox = base.Toolbox()
toolbox.register("getEmpty", getEmpty)
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# создание популяции: функция initRepeat():
# 1. тип контейнера
# 2. ф-я генерирущая объекты, которые помещаются в контейнер
# 3. кол-во объектов, которые помещаются в контейнер
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.getEmpty, ONE_MAX_LENGTH)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


def delDoubl(ind1):
    for i in range(len(ind1)):
        tmp = ind1[i]
        if tmp != empty:
            for k in range(i+1, len(ind1)):
                if ind1[k] == tmp:
                    ind1[k] = empty
    return ind1


def oneMaxFitness(individual):
    value = sum([i[2] for i in individual])
    weight = sum([i[1] for i in individual])
    if weight > 400:
        value = 0
    return value,  # return a tuple # Вернуть кортеж


def mutate(individual, indpb):
    tmp = list(items)
    list.append(tmp, empty)
    ind = random.randint(0, len(items)-1)
    i = random.randint(0, len(individual)-1)
    r = tmp[ind]
    individual[i] = r
    individual = delDoubl(individual)
    return individual,


def mate(ind1, ind2):
    ind1, ind2 = tools.cxTwoPoint(ind1, ind2)
    ind1 = delDoubl(ind1)
    ind2 = delDoubl(ind2)
    return ind1, ind2


toolbox.register("evaluate", oneMaxFitness)
# toolbox.register("select", tools.selRoulette)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", mate)
# toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutate, indpb=INDPB)


def knapsackProblem():
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    population = toolbox.populationCreator(n=POPULATION_SIZE)
    population, logbook = algorithms.eaSimple(population, toolbox,
                                              cxpb=P_CROSSOVER,
                                              mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS,
                                              stats=stats, halloffame=hof,
                                              verbose=True)

    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
    # Nevals представляет количество раз, чтобы вызвать функцию оценки в итерации

    # print("Индивидуумы в зале славы = ", *hof.items, sep="\n")
    value = sum([i[2] for i in hof.items[0]])
    weight = sum([i[1] for i in hof.items[0]])
    print(f'Лучший индивидуум приоритет: {value} вес: {weight}] ')
    tmp = hof.items[0]
    freshIndividuals = [ind for ind in tmp if not ind == empty]
    print(freshIndividuals)


    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    # plt.plot(mutateCounter, color='black', marker='.', linestyle='')
    plt.xlabel('Поколение')
    plt.ylabel('Целевая/средняя приспособленность')
    plt.title('Зависимость целевой и средней приспособленности от поколения')
    plt.show()


if __name__ == '__main__':
    knapsackProblem()
