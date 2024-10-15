def check():
    T = int(input())
    for i in range(1, T+1):
        N = int(input())
        maze = []
        for _ in range(N):
            maze.append(list(input()))
        
        sx, sy, ex, ey = [int(coord) for coord in input().split()]
        
        print(f"Case #{i}: ")

check()