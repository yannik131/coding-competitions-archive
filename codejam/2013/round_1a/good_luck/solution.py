import random
import primefac
import numpy as np
from collections import Counter
from functools import reduce
from operator import mul

def multiply_elements(elements):
    return reduce(mul, elements, 1)

def pad(txt, n=30):
    txt = str(txt)
    return txt + " "*(n-len(txt))

def tuple_to_list(counts):
    return [number for number, count in counts for _ in range(count)]

def add(tuples: set, counter: Counter):
    t = tuple(sorted((number, count) for number, count in counter.items() if count > 0))
    tuples.add(t)

def calculate_number_of_reductions(counter: Counter, n):
    if n == 4:
        return counter[2] // 2
    if n == 6:
        return min(counter[2], counter[3])
    if n == 8:
        return (
            counter[2] // 3,            # 2*2*2=8
            min(counter[2], counter[4]) # 2*4=8
        )
    if n == 9:
        return counter[3] // 2
    
    raise f"n = {n} is not supported"

def reduce_222(counter: Counter, i):
    counter[2] -= i*3
    counter[8] += i

def reduce_24(counter: Counter, i):
    counter[2] -= i
    counter[4] -= i
    counter[8] += i

def reduce_primefactors(counter: Counter, subsets: set, n, limit, calc=None):
    if type(limit) is tuple: # annoying 8
        reduce_primefactors(counter, subsets, 8, limit[0], reduce_222)
        reduce_primefactors(counter, subsets, 8, limit[1], reduce_24)
        return

    for i in range(1, limit+1):
        _counter = counter.copy()
        if n == 4:
            _counter[2] -= i*2
            _counter[4] += i
        elif n == 6:
            _counter[2] -= i
            _counter[3] -= i
            _counter[6] += i
        elif n == 8:
            calc(_counter, i)
        elif n == 9:
            _counter[3] -= i*2
            _counter[9] += i
        
        add(subsets, _counter)

"""
Returns a set of tuples of tuples ((n_i, k_i)) counting how often the number n_i occurs in the list of numbers
"""
def generate_subsets(primefactors, M):
    subsets = set()
    primefactor_counter = Counter(primefactors)
    add(subsets, primefactor_counter)

    prime_products = [4, 6, 8, 9]
    for prime_product in prime_products:
        if M < prime_product:
            break
        for counter in subsets.copy():
            counter = Counter(dict(counter))
            limit = calculate_number_of_reductions(counter, prime_product)
            reduce_primefactors(counter, subsets, prime_product, limit)

    return subsets

def test_subset_generation():
    primefactors = [2, 2, 2, 3, 3, 5]
    possible_results = [
        [2, 4, 5, 9],
        [3, 4, 5, 6],
        [2, 5, 6, 6],
        [2, 2, 2, 3, 3, 5],
        [5, 8, 9],
        [2, 3, 3, 4, 5],
        [3, 3, 5, 8],
        [2, 2, 3, 5, 6],
        [2, 2, 2, 5, 9]
    ]
    possible_results_set = set(tuple(sorted(Counter(numbers).items())) for numbers in possible_results)
    generated_set = generate_subsets(primefactors, 9)

    missing = possible_results_set - generated_set
    unexpected = generated_set - possible_results_set

    if len(missing) > 0:
        print("Missing results:")
        for counts in missing:
            print(tuple_to_list(counts))
    elif len(unexpected) > 0:
        print("Unexpected results:")
        for counts in unexpected:
            print(tuple_to_list(counts))
    else:
        print("Ok")

def generate_products(N, M, K):
    original = sorted([random.randint(2, M) for _ in range(N)])
    products = []

    for _ in range(K):
        subset = []
        for number in original:
            if random.randint(1, 2) == 1:
                continue
            subset.append(number)
        products.append(np.prod(subset))

    return original, products

def guess_numbers(N, M, products):
    total_counter = Counter()

    for product in products:
        #print(f"Processing {product}")
        if product == 1:
            # this does not tell us anything, ignore
            continue
        
        primefactors = list(primefac.primefac(product))
        generated_subsets = generate_subsets(primefactors, M)

        for counts in generated_subsets:
            total_counter += Counter(dict(counts))

    total_sum = sum(total_counter.values())

    probabilities = dict()
    for number, count in total_counter.items():
        probabilities[number] = count / total_sum
    
    guess = random.choices(list(probabilities.keys()), weights=list(probabilities.values()), k=N)
    guess = sorted(guess)

    return guess

def test_guessing(N, M, K, R):
    correct = 0

    for _ in range(R):
        original_numbers, products = generate_products(N, M, K)
        guess = guess_numbers(N, M, products)
        #print(f"Guess: {guess} ", end="")
        #print(f"Numbers: {original_numbers}")
        if guess == original_numbers:
            correct += 1
            #print("-> correct!")

    print(f"Guessed correctly {round(correct / R * 100, 1)}% of the time")
    
#test_subset_generation()
test_guessing(2, 9, 20, 100)
