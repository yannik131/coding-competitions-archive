import random
import numpy as np
from collections import Counter
from functools import reduce
from operator import mul
from math import factorial
from itertools import combinations_with_replacement, combinations

def multiply_elements(elements):
    return reduce(mul, elements, 1)

def pad(txt, n=30):
    txt = str(txt)
    return txt + " "*(n-len(txt))

def generate_products(N, M, K):
    original = sorted([random.randint(2, M) for _ in range(N)])
    products = []

    for _ in range(K):
        subset = []
        for number in original:
            if random.randint(1, 2) == 1:
                continue
            subset.append(number)
        #print(f"{pad(subset)} -> {pad(np.prod(subset), 10)}")
        products.append(np.prod(subset))

    return original, products

# Es werden N Zahlen aus einer Menge von K Zahlen ausgewählt: K^N Möglichkeiten
# Für K = (M - 1) -> (M - 1)^N
# Betrachten wir eine mögliche Auswahl von 12 Zahlen
# Es gibt N! Möglichkeiten N Elemente anzuordnen. Sind unter ihnen r, s, ..., t gleiche Elemente
# gibt es N!/(r!*s!*...*t!) mögliche Anordnungen. Tritt eine Ziffer d N_d mal auf, gibt es also
# N!/(N_2!*N_3!*...*C_M!) mögliche Anordnungen. Die Wahrscheinlichkeit für eine Auswahl ist daher
# N!/(N_2!*N_3!*...*C_M!) / (M - 1)^N
def initial_probability_of(subset, N, M):
    counter = Counter(subset)
    demoninator = multiply_elements([(M-1)**N] + [factorial(count) for count in counter.values()])
    return factorial(N) / demoninator

def guess_numbers(N, M, K, products):
    possible_guesses = [tuple(combination) for combination in combinations_with_replacement(range(2, M+1), N)]
    initial_probabilities = dict() # P(A)
    product_frequencies = dict() # P(p | A)
    product_probabilities = dict() # P(p)
    for guess in possible_guesses:
        initial_probabilities[guess] = initial_probability_of(guess, N, M)
        counter = Counter()
        for i in range(0, N+1):
            for subset in combinations(guess, i):
                counter[np.prod(subset)] += 1
        n_products = sum(counter.values())
        product_frequencies[guess] = dict()
        for product, count in counter.items():
            product_frequencies[guess][product] = count / n_products
            product_probabilities[product] = 0

    for product in product_probabilities:
        for guess in possible_guesses:
            product_probabilities[product] += initial_probabilities[guess] * product_frequencies[guess].get(product, 0)
    
    for product in products:
        for guess in possible_guesses:
            conditional_probability = initial_probabilities[guess] * product_frequencies[guess].get(product, 0) \
                                      / product_probabilities[product] # P(A | p)

            initial_probabilities[guess] *= conditional_probability # P(A) = P(A | p) * P(A) / c_normalization

    guess = list(max(initial_probabilities, key=initial_probabilities.get))
    return guess

def test_guessing(N, M, K, R):
    correct = 0

    for _ in range(R):
        original_numbers, products = generate_products(N, M, K)
        #print(f"Numbers: {original_numbers}")
        guess = guess_numbers(N, M, K, products)
        #print(f"Guess: {guess} ", end="")
        if guess == original_numbers:
            correct += 1
            #print("-> correct!")

    return correct

assert(test_guessing(3, 5, 7, 100) >= 50)
print("Ok - 1")
# this is taking too long with the current
assert(test_guessing(12, 8, 12, 1) >= 1120)
print("Ok - 2")
