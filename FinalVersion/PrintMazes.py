import sys
# from random import random
import random
from copy import copy, deepcopy
from GridRandom50 import TestCaseRandom


random_test_case = TestCaseRandom()

outfile = open('50Mazes.txt','w+')   
for test_case_index in range(len(random_test_case)):      # run 50 random cases for the algorithm comparison (case index: 1 to 49)
    maze = random_test_case.case50[test_case_index].grid
    maze_print = deepcopy(maze)
    for i in range(len(maze_print)):
        for j in range(len(maze_print[i])):
            if maze_print[i][j] == 0:
                maze_print[i][j] = ' '
            elif maze_print[i][j] == 1:
                maze_print[i][j] = 'X'

    print(' ', file=outfile)
    print ('>> ** Maze '+str(test_case_index), file=outfile)
    print(' ', file=outfile)
    for i in range(len(maze_print)):
        for j in range(len(maze_print[i])):
            print(maze_print[i][j], end=' ', file=outfile)
        print()
        print(' ', file=outfile)