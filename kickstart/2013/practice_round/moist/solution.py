def solve(cards):
    # represent the strings as tuples, makes it easy to compare
    # i. e. (1, 1) < (1, 2)
    scores = []
    for card in cards:
        scores.append(tuple(ord(char) for char in card))
    
    n = 0 # number of operations
    i = 0 # current index
    while i < len(scores) - 1:
        #if a card is not in order, find a place for it above and put it there
        if scores[i + 1] < scores[i]:
            value = scores[i + 1]
            j = i
            while j > 0 and value < scores[j]:
                j -= 1
            if value > scores[j]: # missing comparison for j = 0
                j += 1
            score = scores.pop(i + 1)
            scores.insert(j, score)
            
            n += 1
        i += 1

    return n

def check():
    T = int(input())
    for i in range(1, T+1):
        N = int(input())
        cards = []
        for _ in range(N):
            cards.append(input().strip())
        result = solve(cards)
        print(f"Case #{i}: {result}")

check()