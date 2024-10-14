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

def unique_factorizations(N, M):
    def factorize(n, upper_limit, current_factors, results):
        for i in range(2, min(upper_limit, n) + 1):
            if n % i == 0:
                new_factors = current_factors + [i]
                next_n = n // i
                if next_n == 1:
                    results.append(sorted(new_factors))
                else:
                    factorize(next_n, i, new_factors, results)

    results = []
    factorize(N, M, [], results)
    return results

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
    factorizations = unique_factorizations(np.prod(primefactors), 9)
    if sorted(possible_results) != sorted(factorizations):
        raise "Not equal"
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
        
        factorizations = unique_factorizations(product, M)

        for factorization in factorizations:
            total_counter += Counter(factorization)

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
    
test_subset_generation()
test_guessing(4, 9, 3, 10000)