from deap import base
from deap import creator
from deap import tools
import random
import matplotlib.pyplot as plt

# константы задачи
ONE_MAX_LENGTH = 100  # длина подлежащей оптимизации битовой строки
# константы генетического алгоритма
POPULATION_SIZE = 200  # количество индивидуумов в популяции
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.1  # вероятность мутации индивидуума
MAX_GENERATIONS = 50  # максимальное количество поколений

RANDOM_SEED = 42
# на этапе экспериментирования требуется, чтобы результаты были воспроизводимы.
# Для этого мы задаем какое-нибудь фиксированное начальное значение генератора случайных чисел
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()
toolbox.register("zeroOrOne", random.randint, 0, 1)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))

creator.create("Individual", list, fitness=creator.FitnessMax)

#создание популяции: функция initRepeat():
# 1. тип контейнера
# 2. ф-я генерирущая объекты, которые помещаются в контейнер
# 3. кол-во объектов, которые помещаются в контейнер

toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


def oneMaxFitness(individual):
    return sum(individual), # Вернуть кортеж


toolbox.register("evaluate", oneMaxFitness)

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpd=1.0/ONE_MAX_LENGTH)


if __name__ == '__main__':
    population = toolbox.populationCreator(n=POPULATION_SIZE)
    generationCounter = 0
    fitnessValues = list(map(toolbox.evaluate, population))

    for individual, fitnessValue in zip(population, fitnessValues):
        individual.fitness.value = fitnessValue

    fitnessValues = [individual.fitness.value[0] for individual in population]

    maxFitnessValues = []
    meanFitnessValues = []



