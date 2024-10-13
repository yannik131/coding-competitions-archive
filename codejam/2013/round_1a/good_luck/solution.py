import random
import primefac
import numpy as np
from functools import reduce
from operator import mul

def multiply_elements(elements):
    return reduce(mul, elements, 1)

def pad(txt, n=30):
    txt = str(txt)
    return txt + " "*(n-len(txt))

N = 10
M = 8
K = 12

print(f"N = {N}, M = {M}, K = {K}")

numbers = [random.randint(2, M) for _ in range(N)]
subsets = []

for _ in range(K):
    subset = []
    for number in numbers:
        if random.randint(1, 2) == 1:
            continue
        subset.append(number)
    subsets.append(subset)

print(f"Numbers: {numbers}")
print(f"Subsets: ")
products = []
for subset in subsets:
    print(f"{pad(subset)} -> {pad(np.prod(subset), 10)} -> {pad(list(primefac.primefac(np.prod(subset))))}")
    products.append(np.prod(subset))

for product in products:
    print(f"Processing {product}")
    if product == 1:
        # this does not tell us anything, ignore
        print("Product is 1, skip")
        continue
    
    possible_subsets = []
    primefactors = list(primefac.primefac(product))

    for N_ in range(1, len(primefactors) + 1):
        print(f"Generating all possible lists with length {N_}")
        min_factor_value = int(product**(1/N_)) # minimum value for a factor if we want to represent the product
        if min_factor_value > M:
            # value would be too large, ignore
            print(f"Ignoring {N_}, because {N_}th root is {min_factor_value} > {M}")
            continue
        
        diff = len(primefactors) - N_
        min_product = multiply_elements(primefactors[:diff])
        if min_product > M:
            print(f"Ignoring {N_}, because product of smallest {diff} values is {min_product} > {M}")
            continue


        if diff == 0:
            possible_subsets.append(primefactors)
            continue

