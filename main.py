from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as numpy

# константы задачи
ONE_MAX_LENGTH = 100  # длина подлежащей оптимизации битовой строки
MAX_GENERATIONS = 50  # максимальное количество поколений
HALL_OF_FAME_SIZE = 10
# константы генетического алгоритма
POPULATION_SIZE = 200  # количество индивидуумов в популяции
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.1  # вероятность мутации индивидуума
INDPB = 1.0 / ONE_MAX_LENGTH  # вероятность применения мутации к каждоиу биту


RANDOM_SEED = 41
# на этапе экспериментирования требуется, чтобы результаты были воспроизводимы.
# Для этого мы задаем какое-нибудь фиксированное начальное значение генератора случайных чисел
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()
toolbox.register("zeroOrOne", random.randint, 0, 1)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))

creator.create("Individual", list, fitness=creator.FitnessMax)

# создание популяции: функция initRepeat():
# 1. тип контейнера
# 2. ф-я генерирущая объекты, которые помещаются в контейнер
# 3. кол-во объектов, которые помещаются в контейнер

toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


def oneMaxFitness(individual):
    return sum(individual),  # return a tuple # Вернуть кортеж


toolbox.register("evaluate", oneMaxFitness)
# toolbox.register("select", tools.selRoulette)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxTwoPoint)
# toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=INDPB)


def main():
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    generationCounter = 0
    fitnessValues = list(map(toolbox.evaluate, population))

    for individual, fitnessValue in zip(population, fitnessValues):
        individual.fitness.values = fitnessValue

    fitnessValues = [individual.fitness.values[0] for individual in population]

    maxFitnessValues = []
    meanFitnessValues = []
    mutateCounter = []

    while max(fitnessValues) < ONE_MAX_LENGTH and min(fitnessValues) != 0 and generationCounter < MAX_GENERATIONS:
        # while min(fitnessValues) != 0 and generationCounter < MAX_GENERATIONS:
        generationCounter = generationCounter + 1
        # apply the selection operator, to select the next generation's individuals:
        offspring = toolbox.select(population, len(population))
        # clone the selected individuals:
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < P_CROSSOVER:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        mutateCnt = 0
        for mutant in offspring:
            if random.random() < P_MUTATION:
                toolbox.mutate(mutant)
                mutateCnt += 1
                del mutant.fitness.values

        mutateCounter.append(mutateCnt)

        freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
        freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))
        for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
            individual.fitness.values = fitnessValue

        population[:] = offspring

        fitnessValues = [individual.fitness.values[0] for individual in population]

        targetFitness = max(fitnessValues)
        meanFitness = sum(fitnessValues) / len(population)
        maxFitnessValues.append(targetFitness)
        meanFitnessValues.append(meanFitness)
        print("- Поколение {}: Целевая приспособ. = {}, Средняя приспособ. = {}".format(generationCounter, targetFitness,
                                                                                     meanFitness))

        best_index = fitnessValues.index(max(fitnessValues))
        print("Лучший индивидуум = ", *population[best_index], "\n")

    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.plot(mutateCounter, color='black', marker='.', linestyle='')
    plt.xlabel('Поколение')
    plt.ylabel('Целевая/средняя приспособленность')
    plt.title('Зависимость целевой и средней приспособленности от поколения')
    plt.show()


def short_main():

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    population = toolbox.populationCreator(n=POPULATION_SIZE)
    population, logbook = algorithms.eaSimple(population, toolbox,
                                              cxpb=P_CROSSOVER,
                                              mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS,
                                              stats=stats,  halloffame=hof,
                                              verbose=True)

    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")
    # Nevals представляет количество раз, чтобы вызвать функцию оценки в итерации

    # print("Индивидуумы в зале славы = ", *hof.items, sep="\n")
    # print("Лучший индивидуум = ", hof.items[0])
    print("Лучший индивидуум = ", sum(hof.items[0]))

    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    # plt.plot(mutateCounter, color='black', marker='.', linestyle='')
    plt.xlabel('Поколение')
    plt.ylabel('Целевая/средняя приспособленность')
    plt.title('Зависимость целевой и средней приспособленности от поколения')
    plt.show()


if __name__ == '__main__':
    # main()
    short_main()
