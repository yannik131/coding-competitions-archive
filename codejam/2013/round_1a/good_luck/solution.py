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

N = 5
M = 8
K = 5
R = 1000

print(f"N = {N}, M = {M}, K = {K}")

correct = 0

for i in range(R):
    original = sorted([random.randint(2, M) for _ in range(N)])
    subsets = []

    for _ in range(K):
        subset = []
        for number in original:
            if random.randint(1, 2) == 1:
                continue
            subset.append(number)
        subsets.append(subset)

    print(f"Numbers: {original}")
    #print(f"Subsets: ")
    products = []
    for subset in subsets:
        print(f"{pad(subset)} -> {pad(np.prod(subset), 10)} -> {pad(list(primefac.primefac(np.prod(subset))))}")
        products.append(np.prod(subset))

    total = Counter()
    possible_subsets = set()

    def update_total(count):
        #print(f"update_total {count}")
        possible_subsets.add(tuple(sorted(count.items())))
        total.update(count)
        
    for product in products:
        #print(f"Processing {product}")
        if product == 1:
            # this does not tell us anything, ignore
            #print("Product is 1, skip")
            continue
        
        primefactors = list(primefac.primefac(product))
        
        primefactor_counts = Counter(primefactors)
        
        update_total(primefactor_counts)

        # only numbers smaller than 10 which are products of primes are 2*2=4, 2*3=6, 2*2*2=8 and 3*3=9

        if M >= 4:
            for counts in possible_subsets.copy():
                counts = Counter(dict(counts))
                n_4 = counts[2] // 2 # this is how many 4's we can create
                for i in range(1, n_4+1):
                    _counts = counts.copy()
                    _counts[2] -= i*2
                    _counts[4] += i
                    update_total(_counts)

        if M >= 6:
            for counts in possible_subsets.copy():
                counts = Counter(dict(counts))
                n_6 = min(counts[2], counts[3])
                for i in range(1, n_6+1):
                    _counts = counts.copy()
                    _counts[2] -= i
                    _counts[3] -= i
                    _counts[6] += i
                    update_total(_counts)

        if M >= 8:
            for counts in possible_subsets.copy():
                counts = Counter(dict(counts))
                n_8 = counts[2] // 3
                for i in range(1, n_8+1):
                    _counts = counts.copy()
                    _counts[2] -= i*3
                    _counts[8] += i
                    update_total(_counts)

            for counts in possible_subsets.copy():
                counts = Counter(dict(counts))
                n_8 = min(counts[2], counts[4])
                for i in range(1, n_8+1):
                    _counts = counts.copy()
                    _counts[2] -= i
                    _counts[4] -= i
                    _counts[8] += i
                    update_total(_counts)

        if M >= 9:
            for counts in possible_subsets.copy():
                counts = Counter(dict(counts))
                n_9 = counts[3] // 2
                for i in range(1, n_9+1):
                    _counts = counts.copy()
                    _counts[3] -= i*2
                    _counts[9] += i
                    update_total(_counts)

        """for subset in possible_subsets:
            subset_dict = dict(subset)
            numbers = [num for num, count in subset_dict.items() for _ in range(count)]
            print(numbers)"""

    total_counts = sum(total.values())
    print(total, total_counts)
    if total_counts == 0:
        for subset in subsets:
            print(f"{pad(subset)} -> {pad(np.prod(subset), 10)} -> {pad(list(primefac.primefac(np.prod(subset))))}")
        continue
    probabilities = dict()
    for number in total:
        probabilities[number] = total[number] / total_counts
    
    guess = random.choices(list(probabilities.keys()), weights=list(probabilities.values()), k=N)
    guess = sorted(guess)

    print(f"Guess: {guess} ", end="")
    if guess == original:
        correct += 1
        print("-> correct!")
    else:
        print("-> wrong!")

print(f"Guessed correctly {round(correct / R * 100, 1)}% of the time")