'''
Fitness Function : f(x) = x^2 + 5
Algorithm = Gene Algorithm (GA)
'''

import random
from bitarray import bitarray
import struct
import  random

random.seed(0)
NUM_CHROM = 20
NUM_BIT = 100
MAX_NUM_GENERATION = 2000

class Population():
    bit = bitarray(random.randint(0,1) * NUM_BIT, endian='little')
    fit = 0

def y(x):
    value = int(x.bit.to01(),2)
    return -value * value + 5

def spr_y(spring):
    value = int(spring.to01(),2)
    return -value * value + 5

def Tournament(x):
    x_fit = [y(x[i]) for i in range(NUM_CHROM)]
    for i in range(NUM_CHROM): x[i].fit = x_fit[i]
    x_index = [i for i in range(NUM_CHROM)]
    x_fit, x_index = zip(*sorted(zip(x_fit,x_index),reverse = True))

    return [x[i] for i in x_index]

def Single_point(x):
    rnd_position = random.randint(1, NUM_BIT-1)

    #第一條子代
    Spring_1 = bitarray('0' * NUM_BIT, endian='little')
    #第二條子代
    Spring_2 = bitarray('0' * NUM_BIT, endian='little')
    for i in range(rnd_position):
        Spring_1[i] = Spring_1[i] | x[0].bit[i]
        Spring_2[i] = Spring_2[i] | x[1].bit[i]

    for j in range(rnd_position, NUM_BIT):
        Spring_1[j] = Spring_1[j] | x[1].bit[j]
        Spring_2[j] = Spring_2[j] | x[0].bit[j]

    return  Spring_1, Spring_2

def Multi_point(x):
    rnd_position_one = 1
    rnd_position_two = 2

    while rnd_position_one - rnd_position_two < 2:
        rnd_position_one = random.randint(1, NUM_BIT-1)
        rnd_position_two = random.randint(1, NUM_BIT-1)


    #第一條子代
    Spring_1 = bitarray('0' * NUM_BIT, endian='little')
    #第二條子代
    Spring_2 = bitarray('0' * NUM_BIT, endian='little')

    for i in range(rnd_position_one):
        Spring_1[i] = Spring_1[i] | x[0].bit[i]
        Spring_2[i] = Spring_2[i] | x[1].bit[i]

    for j in range(rnd_position_one, rnd_position_two):
        Spring_1[j] = Spring_1[j] | x[1].bit[j]
        Spring_2[j] = Spring_2[j] | x[0].bit[j]

    for k in range(rnd_position_two, NUM_BIT):
        Spring_1[k] = Spring_1[k] | x[0].bit[k]
        Spring_2[k] = Spring_2[k] | x[1].bit[k]


    return  Spring_1, Spring_2


def Mutation(Spring_1, Spring_2):
    rnd = random.uniform(0,1)                  #發生突變機率
    rnd_pos = random.randint(1,NUM_BIT - 1)      #突變的BIT
    if (rnd >= 0.4):
        Spring_1[rnd_pos] = random.randint(0,1)
        Spring_2[rnd_pos] = random.randint(0,1)
    return  Spring_1, Spring_2

def Replace(x, Spring_1, Spring_2):

    spr1_fit = spr_y(Spring_1)
    spr2_fit = spr_y(Spring_2)

    if (spr1_fit >= x[NUM_CHROM-2].fit): x[NUM_CHROM-2].bit = Spring_1
    elif (spr1_fit >= x[NUM_CHROM-1].fit): x[NUM_CHROM-1].bit = Spring_1

    if (spr2_fit >= x[NUM_CHROM-2].fit):
        x[NUM_CHROM-2].bit = Spring_2
        x[NUM_CHROM-1].bit = Spring_1
    elif (spr2_fit >= x[NUM_CHROM-1].fit): x[NUM_CHROM-1].bit = Spring_2


    return x

# Create four chromosomes
x = [Population()for i in range(NUM_CHROM)]
for i in range(NUM_CHROM):
    x[i].fit  = y(x[i])

# Main Code
for i in range(MAX_NUM_GENERATION):
    x_next = Tournament(x)                      #得到(Fittness)由大到小排序過後的染色體
    spring_1, spring_2 = Single_point(x_next)   #單點交配
    spring_1, spring_2 = Multi_point(x_next)   #多點交配
    spring_1, spring_2 = Mutation(spring_1, spring_2)
    x_next = Replace(x_next, spring_1, spring_2)
    print(x_next[0].fit)
print("Finished!!!!!!!!!")
