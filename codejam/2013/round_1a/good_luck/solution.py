import random
import numpy as np
from collections import Counter
from math import factorial
from itertools import combinations_with_replacement, combinations


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
        #print(f"{pad(subset)} -> {pad(np.prod(subset).astype(int), 10)}")
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
    demoninator = np.prod([(M-1)**N] + [factorial(count) for count in counter.values()])
    return factorial(N) / demoninator

def in_order(array):
    counter = Counter(sorted(array))
    while len(counter) > 0:
        _counter = counter.copy()
        for value in _counter:
            counter[value] -= 1
            if counter[value] == 0:
                del counter[value]
            yield value

def count_product_combinations(array):
    product_counts = Counter()
    product_counts[1] = 1  # The empty subset product

    for num in array:
        current_counts = list(product_counts.items())
        for product, count in current_counts:
            new_product = product * num
            product_counts[new_product] += count
    
    return product_counts

def guess_numbers(N, M, products):
    possible_guesses = set(tuple(combination) for combination in combinations_with_replacement(range(2, M+1), N))
    initial_probabilities = dict() # P(A)
    product_frequencies = dict() # P(p | A)
    product_probabilities = dict() # P(p)
    for guess in possible_guesses:
        initial_probabilities[guess] = initial_probability_of(guess, N, M)
        counter = count_product_combinations(guess)
        n_products = sum(counter.values())
        product_frequencies[guess] = dict()
        for product, count in counter.items():
            product_frequencies[guess][product] = count / n_products
            product_probabilities[product] = 0
    for guess in possible_guesses:
        for product, frequency in product_frequencies[guess].items():
            product_probabilities[product] += initial_probabilities[guess] * frequency
    
    for product in in_order(products):
        if product == 1:
            continue
        for guess in possible_guesses.copy():
            conditional_probability = initial_probabilities[guess] * product_frequencies[guess].get(product, 0) \
                                      / product_probabilities.get(product, 0) # P(A | p)
            initial_probabilities[guess] *= conditional_probability # P(A) = P(A | p) * P(A) / c_normalization

        total_sum = sum(initial_probabilities.values())

        c = 1.0/total_sum
        if np.isnan(c):
            # oops - we probably eliminated a guess already because of previous products
            # this can easily happen due to very small probabilities for large N
            return None
        for guess in possible_guesses.copy():
            initial_probabilities[guess] *= c # normalize the probabilities again
            if initial_probabilities[guess] < 10**-200:
                del initial_probabilities[guess]
                possible_guesses.remove(guess)

        if len(possible_guesses) == 1:
            break
        
    #print(sorted(initial_probabilities.items(), key=lambda item: item[1], reverse=True)[:5])
    guess = list(max(initial_probabilities, key=initial_probabilities.get))
    return guess

def test_guessing(N, M, K, R):
    correct = 0

    for _ in range(R):
        original_numbers, products = generate_products(N, M, K)
        #print(f"Numbers: {original_numbers}")
        guess = guess_numbers(N, M, products)
        #print(f"Guess: {guess} ")
        if guess == original_numbers:
            correct += 1
            #print("-> correct!")

    return correct

assert(test_guessing(3, 5, 7, 100) >= 50)
print("Small dataset - OK")
# this is taking too long with the current implementation
assert(test_guessing(12, 8, 12, 8000) >= 1120)

print("Large dataset - OK")
