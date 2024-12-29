import numpy
import math

total_race=100
least_win_race=53
prediction_accuracy=0.57
probability=0

for i in range(least_win_race,total_race):
    probability+=numpy.float_power(prediction_accuracy,i)*numpy.float_power(1-prediction_accuracy,total_race-i)*math.comb(total_race,i)

print(probability)
