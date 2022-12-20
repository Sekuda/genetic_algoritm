from deap import creator
from deap import base

creator.create("FitnessMax", base.Fitness, weights=(1.0,))

