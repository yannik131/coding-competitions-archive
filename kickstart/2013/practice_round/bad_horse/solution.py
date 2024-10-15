import networkx as nx

# https://de.wikipedia.org/wiki/Bipartiter_Graph
def solve(test_case):
    graph = nx.Graph()
    edges = [names.split() for names in test_case]
    graph.add_edges_from(edges)
    
    if nx.is_bipartite(graph):
        return "Yes"
    return "No"

def check():
    T = int(input())
    for i in range(1, T+1):
        M = int(input())
        names = []
        for _ in range(M):
            names.append(input().strip())
        result = solve(names)
        print(f"Case #{i}: {result}")

check()