#!/bin/python3

import math
import os
import random
import re
import sys
import numpy as np



#
# Complete the 'maximumProfit' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts INTEGER_ARRAY price as parameter.
#

def maximumProfit(price):
    sorted_inds = list(np.argsort(price))
    max_ind = sorted_inds.pop()
    profit = 0
    shares = 0
    
    for i, p in enumerate(price):
        if i > max_ind:
            while True:
                if sorted_inds:
                    max_ind = sorted_inds.pop()
                    if i <= max_ind:
                        break
                else:
                    return profit
        
        if i == max_ind:
            profit += shares * p
            shares = 0
            while True:
                if sorted_inds:
                    max_ind = sorted_inds.pop()
                    if i <= max_ind:
                        break
                else:
                    return profit
        
        else:
            profit -= p
            shares += 1
    
    return profit



if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        price = list(map(int, input().rstrip().split()))

        profit = maximumProfit(price)

        fptr.write(str(profit) + '\n')

    fptr.close()