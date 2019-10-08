import random

def drawGrid():
    grid = []
    for rows in range(26):
        grid.append([])
        for cols in range(26):
            grid[rows].append(0)
    return grid

def startState(grid):
    x = random.randint(0, len(grid))
    y = random.randint(0, len(grid))
    while(grid[x][y] == 'X' or grid[x][y] == 'g'):
        x = random.randint(0, len(grid))
        y = random.randint(0, len(grid))
    grid[x][y] = 's'

def goalState(grid):
    x = random.randint(0, len(grid))
    y = random.randint(0, len(grid))
    while(grid[x][y] == 'X' or grid[x][y] == 's'):
        x = random.randint(0, len(grid))
        y = random.randint(0, len(grid))
    grid[x][y] = 'g'


def createBlocks(grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            if(random.random() > 0.7):
                #blocked
                grid[x][y] = 'X'
            else:
                #open
                grid[x][y] = '-'

def printGraph(grid):
    for x in range (len(grid)):
        for y in range (len(grid[x])):
            print(grid[x][y], end = " ")
        print()


grid = drawGrid()
createBlocks(grid)
startState(grid)
goalState(grid)
printGraph(grid)
