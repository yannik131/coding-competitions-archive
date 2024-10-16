MOVE_FORWARD_MAP = {
    "E": lambda x, y: (x+1, y),
    "W": lambda x, y: (x-1, y),
    "N": lambda x, y: (x, y-1),
    "S": lambda x, y: (x, y+1)
}

TURN_RIGHT_MAP = {
    "E": "S",
    "S": "W",
    "W": "N",
    "N": "E"
}

TURN_LEFT_MAP = {
    "E": "N",
    "N": "W",
    "W": "S",
    "S": "E"
}

def is_out_of_bounds(maze, x, y):
    return x < 0 or y < 0 or x == len(maze) or y == len(maze)

def left(maze, x, y, direction):
    x, y = MOVE_FORWARD_MAP[TURN_LEFT_MAP[direction]](x, y)
    if is_out_of_bounds(maze, x, y):
        return '#'
    return maze[y][x]

def turn_necessary(maze, x, y, direction):
    if left(maze, x, y, direction) != "#":
        return True
    x, y = MOVE_FORWARD_MAP[direction](x, y)
    if is_out_of_bounds(maze, x, y) or maze[y][x] == "#":
        return True
    return False

def turn(maze, x, y, direction):
    if left(maze, x, y, direction) != "#":
        return TURN_LEFT_MAP[direction]
    
    next_direction = TURN_RIGHT_MAP[direction]
    while turn_necessary(maze, x, y, next_direction) and next_direction != direction:
        next_direction = TURN_RIGHT_MAP[next_direction]

    if next_direction == direction:
        return None
    return next_direction

def get_initial_direction(maze, x, y):
    direction = "E"
    while not left(maze, x, y, direction) == "#":
        direction = TURN_RIGHT_MAP[direction]
        if direction == "E":
            raise "Can't set up initial position!"
    return direction

def solve(maze, x, y, end):
    direction = get_initial_direction(maze, x, y)
    solution = ""
    i = 0
    while i < 10000:
        if turn_necessary(maze, x, y, direction):
            direction = turn(maze, x, y, direction)
            if direction is None:
                break
        x, y = MOVE_FORWARD_MAP[direction](x, y)
        solution += direction
        i += 1
        if (x, y) == end:
            return f"{i}\n{solution}"
            
    return "Edison ran out of energy."


def check(subtask, solve):
    with open(f"./data/secret/{subtask}/1.in") as file:
        test_data = file.readlines()
    with open(f"./data/secret/{subtask}/1.ans") as file:
        answers = []
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.endswith("energy."):
                answers.append(line)
            else:
                answers.append(line + "\n" + lines[i+1].strip())
                i += 1
            i += 1
        
        
    T = int(test_data[0].strip())
    N = -1
    test_cases = []
    maze = []
    for line in test_data[1:]:
        if N == 0:
            sx, sy, ex, ey = [int(coord) for coord in line.strip().split()]
            test_cases.append((maze, (sy-1, sx-1, (ey-1, ex-1))))
            maze = []
        elif N == -1:
            N = int(line.strip()) + 1
        else:
            maze.append(line.strip())
        
        N -= 1

    for i, answer in enumerate(answers):
        answer = answer.strip()
        result = solve(test_cases[i][0], *test_cases[i][1])
        result = f"Case #{i+1}: {result}"
        if answer != result:
            print(f"Test case #{i+1} not handled correctly, expected \"{answer}\", got \"{result}\" instead")
            print(*test_cases[i])
            return
    
    print(f"{subtask} - Ok")

check("subtask1", solve)
check("subtask2", solve)