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