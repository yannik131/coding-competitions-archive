import numpy as np
import re

def check(solve, subtask):
    with open(f"./2013/practice_round/captain_hammer/data/secret/{subtask}/1.in") as file:
        test_data = file.readlines()
    with open(f"./2013/practice_round/captain_hammer/data/secret/{subtask}/1.ans") as file:
        answers = file.readlines()
        
    test_cases = []
    test_cases = []
    for line in test_data[1:]:
        V, D = line.split()
        test_cases.append([int(V), int(D)])
        
    regexpr = re.compile(r"(\d+\.\d+)")
    for i, answer in enumerate(answers):
        answer = answer.strip()
        match = re.findall(regexpr, answer)
        answer = float(match[0])
        result = solve(*test_cases[i])
        if abs(result - answer) > 10**-6:
            print(f"Test case #{i+1} not handled correctly, expected \"{answer}\", got \"{result}\" instead")
            print(*test_cases[i])
            return
    
    print("Ok")

def solve(V, D):
    return np.arcsin(D*9.8/V**2)/2/np.pi*180

check(solve, "subtask1")