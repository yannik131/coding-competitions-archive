def check(solve, subtask):
    with open(f"./2013/practice_round/moist/data/secret/{subtask}/1.in") as file:
        test_data = file.readlines()
    with open(f"./2013/practice_round/moist/data/secret/{subtask}/1.ans") as file:
        answers = file.readlines()
        
    test_cases = []
    n = 0
    for line in test_data[1:]:
        if n == 0:
            n = int(line)
            test_cases.append([])
        else:
            test_cases[-1].append(line.strip())
            n -= 1
        
    for i, answer in enumerate(answers):
        answer = answer.strip()
        result = solve(test_cases[i])
        result = f"Case #{i+1}: {result}"
        if result != answer:
            print(f"Test case #{i+1} not handled correctly, expected \"{answer}\", got \"{result}\" instead")
            print(test_cases[i])
            return
    
    print("Ok")

def solve(cards):
    scores = []
    for card in cards:
        scores.append(tuple(ord(char) for char in card))
    
    n = 0
    i = 0
    while i < len(scores) - 1:
        if scores[i + 1] < scores[i]:
            value = scores[i + 1]
            j = i
            while j > 0 and value < scores[j]:
                j -= 1
            if value > scores[j]:
                j += 1
            card = cards.pop(i + 1)
            cards.insert(j, card)
            score = scores.pop(i + 1)
            scores.insert(j, score)
            
            n += 1
        i += 1

    return n


check(solve, "subtask1")
check(solve, "subtask2")