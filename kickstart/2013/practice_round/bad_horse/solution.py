import networkx as nx

def check(solve, subtask):
    with open(f"./2013/practice_round/bad_horse/data/secret/{subtask}/1.in") as file:
        test_data = file.readlines()
    with open(f"./2013/practice_round/bad_horse/data/secret/{subtask}/1.ans") as file:
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

# https://de.wikipedia.org/wiki/Bipartiter_Graph
def solve(test_case):
    graph = nx.Graph()
    edges = [names.split() for names in test_case]
    graph.add_edges_from(edges)
    
    if nx.is_bipartite(graph):
        return "Yes"
    return "No"

check(solve, "subtask1")
check(solve, "subtask2")