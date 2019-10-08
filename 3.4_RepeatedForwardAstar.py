import sys
from random import random
from copy import copy, deepcopy

class Node():
    """A node class for A* """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# get current node's children list based on its valid actions 
# assuming that actions to and from the "known" blocked cells were eliminated  
def get_children(current_node, maze, block_tag, children):
    """get current node's children list based on its valid actions"""
    # Generate children
    children = []
    # check actions
    # left (0, -1); right (0, 1); up (-1, 0); down (1, 0)
    succ_position_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # calculate valid actions
    # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
    for new_position in succ_position_list: # Adjacent squares

        # Get the node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure it is within the range
        if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
            continue

        # Make sure it is not the parent of the current_node
        if current_node.parent and (current_node.parent.position ==  node_position):
            continue

        # Make sure it is walkable terrain
        if maze[node_position[0]][node_position[1]][0] == block_tag:
            continue

        # Create a new node
        new_node = Node(current_node, node_position)

        # Append
        children.append(new_node)

    return children

def astar(maze, start_node, end_node, block_tag, counter):
    """Returns a list of tuples as a path from start to end in the given maze"""

    global open_list
    global closed_list

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
            elif (item.f == current_node.f) and (item.g > current_node.g):  # tie breaker, get high g(s)
            # elif (item.f == current_node.f) and (item.g < current_node.g):  # tie breaker, get low g(s)
                current_node = item
                current_index = index

        # goal test, if it is the goal, return the path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # expand current node: 
        # pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Generate children
        children = []
        children = get_children(current_node, maze, block_tag, children)

        # Loop through the children
        for child in children:
            # # Child is on the closed list
            # in_closed_list = 0
            # for closed_child in closed_list:
            #     if child == closed_child:
            #         in_closed_list = 1
            #         break
            # if in_closed_list == 1:
            #     continue

            # initialize the child node
            child.g = current_node.g + 1
            if maze[child.position[0]][child.position[1]][2] == -1:
                child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            else:
                child.h = maze[child.position[0]][child.position[1]][2]     # take h(s) override (by Adaptive A*)
            child.f = child.g + child.h

            # ** use [search(s) + counter]
            #    1) to initialize g(s) only when encountered
            #    2) to check if the child has been "encountered" in the current search
            #       if not, it is neither in CLOSED nor in OPEN
            # An expanded child node should be in one of 3 situations below:
            #    1) has never been "encountered" in the current search 
            #       >> to do: append the node to open_list
            #    2) in open_list 
            #       >> to do: replace the node in open_list if child g(s) is smaller
            #    3) in closed_list, or "was in open_list and replaced by one with a lower g value
            #       >> do nothing
            # efficiency considerations:
            #    1) initialize g(s) only when encountered (use search(s) + counter)
            #    2) no need to check if a child is in closed_list by a sequential search 
            #       ** do nothing to the child node 
            #          if 1) search(child) == counter and 2) child not in open_list  
            is_first_encounter = 0
            if maze[child.position[0]][child.position[1]][1] < counter:
                maze[child.position[0]][child.position[1]][1] = counter
                is_first_encounter = 1

            if is_first_encounter == 1:
                open_list.append(child)
                continue

            # check if "child" state is in the open_list
            # "replace" the element in open_list with "child" if 
            #   1) the "child" state is in open_list and 
            #   2) child.g < element.g
            #   >> keep the one with the low g(s) value in open_list
            in_open_list = 0
            for count, elem in enumerate(open_list):
                if child == elem:
                    in_open_list = 1
                    if child.g < elem.g:
                        open_list.pop(count)
                        open_list.append(child)
            if in_open_list == 1:
                continue                    

# -----------------------------------------------------------------------------------------
# function: move_agent_from_start_to_goal()
# -----------------------------------------------------------------------------------------
# >> return value
#    1) assume that the start cell is not blocked
#    2) if the end is reached, return agent_position = end
#    3) if a blocked cell is encountered, 
#       return agent_position right before the blocked cell
# >> move along the path, and stop if it hits a blocked cell: 
#    1) set the blocked cell to have the blocked_value to 2
#       to represent (blocked and "known to agent")
#    2) for "adaptive A*" only:
#       update heuritics h(s) for all nodes in closed_list
#       >> with a more accurate heuristics
#       >> for later search "efficiency"
# -----------------------------------------------------------------------------------------
def move_agent_from_start_to_goal(maze_knowledge, start, end, path, block_tag):
    prior_position = path[0]
    for i in range(len(path)):
        if maze_knowledge[path[i][0]][path[i][1]][0] >= block_tag:
            # mark path[i] cell as "blocked and known"
            # 1) 0: un-blocked 
            # 2) 1: blocked (but not known to agent)
            # 3) 2: blocked and "known to agent"  
            maze_knowledge[path[i][0]][path[i][1]][0] = 2

            # >> "Adaptive A*" algorithm is enforced here:
            #    update grid cell heuristic h(s): for all nodes in closed_list   
            # for i in range(len(closed_list)):
            #     g_goal = len(path) - 1
            #     maze_knowledge[closed_list[i].position[0]][closed_list[i].position[1]][2] = g_goal - closed_list[i].g

            break

        prior_position = path[i]

    return prior_position

def gen_maze():

    # a test grid generated with 30% randomly blocked cells 
    m001 = [[0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1,0,0,1,1,1,0,0,0,0,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0],
            [0,0,1,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,0,0,1,1,0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,1,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0],
            [0,0,1,0,0,0,1,1,0,1,1,1,0,1,0,0,1,1,0,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,0,0,1,1,0,0,1,1,0,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,1,1,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,1],
            [1,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,0],
            [1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,1,1,1,1,1,0,0,0,0,0,1,0,0,1,0,1,1,0,1,0,1,0,0,1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0,1,0,1,0,1,0,1,1,0,0,1,0],
            [1,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,1,0,0,1,0,0,1,0,1,1,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0],
            [0,1,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,0,0,1,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,0,0,1,1,1,0,0,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,1,1,1,0,1,0],
            [0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,1,0,0,1,0,0,1],
            [1,0,1,0,0,0,1,1,1,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,1,1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1],
            [1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0,1,1,1,0,0,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0],
            [1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1,1,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0],
            [1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,1,0,0,1,1],
            [1,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,1,1,0,1,0,0,1,1],
            [0,1,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0],
            [0,1,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0],
            [1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0],
            [1,0,1,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,1,0,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,1,1,0,1,1,0,0,0,0,1,0,1,0,0,1,1,0],
            [0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,0,1,0,1,0],
            [0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0],
            [0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,1,1,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
            [0,0,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0],
            [1,0,0,1,0,0,0,1,0,1,0,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,1,1,0,1,0,1,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0],
            [0,0,1,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,1,1,0,1,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,0,0],
            [0,1,0,0,0,1,1,0,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,0,0,1,0,0],
            [1,0,0,0,1,1,0,1,0,0,1,0,1,0,0,1,1,0,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,1,1,1,1,1,1,0,0,0,0],
            [0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,1,0],
            [0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,0,1,0,0,1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,1,1,1,0,0,0,0,1,0,0],
            [0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0],
            [0,0,1,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,1,1,1,1,0,0,0,1,0,1,1,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,1,1,0,1],
            [1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0],
            [1,1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,1,0,1,1,0,0,1,1,0,1,0,1,1,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0],
            [1,0,0,0,1,0,0,1,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,0,1],
            [1,0,1,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1],
            [0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,0,0],
            [1,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,0,1,1,0,1,1,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,0,1,0,0,0,0,1,0,1,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
            [0,1,1,0,1,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1],
            [0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0],
            [1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0],
            [1,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0],
            [0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0],
            [1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0],
            [1,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,0,1,1,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,0,1,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
            [0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0],
            [0,0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,1,1,1,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,1,1,0,1,1,0,0,0,0,1,1,1,0,0,0,1,0,1,0,0,1,1,1],
            [1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,0],
            [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0,1,1,1,1,0,1,1,0,0,0,0],
            [0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,1,0,1,0,0,0,0,1,0,0,0,1,0,1,1,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,1,0,0,1,1,1,1,0,1,1,0,0,0,0,0,1,0,1,1,0,1,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1],
            [1,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,0,0,1,1,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0],
            [1,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,0,0,0,0,1,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,1,0],
            [0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,0,1,1,1,1,1,0,0,0,1,1,1,0,0,1,0,1,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0],
            [0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
            [0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,0,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,1,1,1,1,0,0,0,0,0,1,1,0],
            [1,0,0,0,1,1,1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,1,0,0,1,0,1,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,0,1,1,1,1,0,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,1,1,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0],
            [1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1],
            [0,0,0,0,0,1,1,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,1,1,0,1,0,0,0,1,0,0,0,1,1,0],
            [0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,0,1,0,0,1,0,1,1,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1,0,0,1],
            [0,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,0,1,1,0],
            [0,0,0,1,1,0,1,0,1,0,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,1],
            [0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,0],
            [0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,1,1,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,0,1,0,1,0,1,0,1,0],
            [0,1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,1,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,1,0,0,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0],
            [0,1,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0],
            [0,1,0,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,0,0,0,0,1,0],
            [1,0,0,0,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,0],
            [1,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,1,1,1,1,0,0,0,0],
            [0,0,0,0,1,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0,0,0,1,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0],
            [0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,1,1,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0],
            [1,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,1,0,1,0,0,1,0,1,1,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,0,0,1,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,1],
            [0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,0,1,1,0,1,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,1],
            [0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,1,1,0,1,0,1,0,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0],
            [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,1,1,1,0,1,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0],
            [0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1],
            [0,1,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,1,1,1,0,0,1,0,1,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0],
            [0,0,1,0,1,0,0,1,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,1,0,1,1,1,1,0,0,0,0,0,1,0,0],
            [1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,1],
            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0],
            [0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,1,0,1,0]]

    # maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    return m001

# def drawGrid():
#     grid = []
#     for rows in range(101):
#         grid.append([])
#         for cols in range(101):
#             grid[rows].append(0)
#     return grid

# def startState(grid):
#     x = random.randint(0, len(grid))
#     y = random.randint(0, len(grid))
#     grid[x][y] = 's'

# def goalState(grid):
#     x = random.randint(0, len(grid))
#     y = random.randint(0, len(grid))
#     grid[x][y] = 'x'

def createBlocks(grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            if(random() > 0.7):
                #blocked
                grid[x][y] = 1
            else:
                #open
                grid[x][y] = 0
    return grid

# global:
# Initialize both the open and closed lists
open_list = []
closed_list = []

def main():
    counter = 0
    grand_path = []
    grand_expanded_cell_count = 0

    # Initialize both the open and closed lists
    global open_list
    global closed_list

    open_list = []
    closed_list = []

    maze = gen_maze()
    # maze = createBlocks(maze)

    # initial_start = (0, 0)
    # start = initial_start
    # end = (7, 6)
    # end = (100, 100)

    # ** the below code is temporary:
    #   for making cases for testing 
    #   in 101 x 101 grid  
    start = (0, 0)                          # manually set start and end for testing
    end = (97, 96)
    if maze[start[0]][start[1]] == 1:       # make sure start cell is not blocked
        maze[start[0]][start[1]] = 0
    if maze[end[0]][end[1]] == 1:           # make sure end cell is not blocked
        maze[end[0]][end[1]] = 0

    print()
    print ('>>> maze (input)')
    for i in range(len(maze)):
        # print('[',end='')
        for j in range(len(maze[i])):
            print(maze[i][j], end=' ')
            # print(maze[i][j], end=',')
        print()
        # print(']')

    # test if the start cell is blocked
    if maze[start[0]][start[1]] == 1 or maze[end[0]][end[1]] == 1:
        print('>>> Either the start or end cell is blocked')
        print('>>> Program exiting')
        exit()

    # -------------------------------------------------------------------------
    # initialize maze_knowledge
    # -------------------------------------------------------------------------
    # ** maze_knowledge represents an "environment"
    #      with a knowledge base learned overtime 
    # ** Each cell have 3 values associated:
    #      [blocked(s), search(s), heuristic(s)]
    #    1) blocked(s) = 
    #       0: not blocked, 1: blocked but not learned, 2: blocked and learned 
    #    2) search(s) = (0, 1, 2... "n-th" ...) 
    #       the state s is "encountered" in the n-th search 
    #    3) heuristic(s), used in A* adaptive,
    #       (1) not used in the beginning, 
    #           no initialization with precalculated h(s) value for each cell
    #       (2) this is used only in adaptive A* 
    #           when a better h(s) is known for a cell
    #       (3) if no h(s) value is stored for the cell, 
    #           calculate the manhattan distance in run time for h(s)
    #       ** Therefore:
    #       if value = -1: calculate the manhattan distance in runtime, 
    #       else: use the better h(s) override from adaptive A*  
    # ** The final agent travel path is collected progressively 
    #    from one search to another in a global variable "grand_path"
    #    1) each A* search returns a path, which is acquired by  
    #       following the A* search tree node pointers 
    #       from the goal node back to the start node   
    #    2) the program then tries to move the agent along that path
    #    3) if a cell is blocked in the middle, 
    #       A* is called again starting from the cell right before the blocked cell
    #       and the agent travel path "grand_path" is extended accordingly.
    # -------------------------------------------------------------------------
    print()
    print ('>>> maze (initialized, with knowledge base)')
    maze_knowledge = deepcopy(maze)
    for i in range(len(maze_knowledge)):
        for j in range(len(maze_knowledge[i])):
            maze_knowledge[i][j] = [maze_knowledge[i][j],0,-1]
            # maze_knowledge[i][j] = [maze_knowledge[i][j],0,-1,-1]
            # print(maze_knowledge[i][j], end=' ')
        # print()

    while start != end:
        counter = counter + 1

        # Create the start and end nodes
        start_node = Node(None, start)
        # initialize start_node.g
        start_node.g = 0
        start_node.h = abs(start[0] - end[0]) + abs(start[1] - end[1])
        start_node.f = start_node.g + start_node.h 
        
        # initialize end_node.g
        end_node = Node(None, end)
        end_node.g = -99        # -99 represents infinity  

        # Initialize both the open and closed lists
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)
        maze_knowledge[start_node.position[0]][start_node.position[1]][1]=counter    # search(s_start)

        block_tag = 2       # observe only "known" blocked cells 
        path = astar(maze_knowledge, start_node, end_node, block_tag, counter)
        if (len(open_list) == 0) or (not path):
            print('>>> program termination condition encountered:')
            if (len(open_list) == 0):
                print('    open_list is empty; there is no node to expand for reaching the goal.')
            if not path:
                print('    no path returned from A*.')
            print('>>> Program exiting')
            break

        # print path >> after astar()
        print()
        print ('>>> invoke astar()...')
        print('    ** counter = ' + str(counter) + '; result search path = ' + str(path))

        # # print maze_knowledge >> after astar()
        # # print ('print maze_knowledge >> after astar()')
        # for i in range(len(maze_knowledge)):
        #     for j in range(len(maze_knowledge[i])):
        #         print(maze_knowledge[i][j], end=' ')
        #     print()

        print('>>> move_agent_from_start_to_goal()')
        block_tag = 1       # observe all blocked cells in reality (known + unkown) 
        # function: move_agent_from_start_to_goal()
        # >> move along the path, stop if it hits a blocked cell 
        # 1) assume start cell is not blocked
        # 2) if blocked cell is encountered, return agent_position right before the blocked cell
        # 3) if the end is reached, return agent_position = end
        agent_position = move_agent_from_start_to_goal(maze_knowledge, start, end, path, block_tag)

        # print maze_knowledge >> after move_agent_from_start_to_goal()
        # print ('print maze_knowledge >> after move_agent_from_start_to_goal()')
        # for i in range(len(maze_knowledge)):
        #     for j in range(len(maze_knowledge[i])):
        #         print(maze_knowledge[i][j], end=' ')
        #     print()
        
        # goal test
        if agent_position == end:
            grand_path = grand_path + path
            grand_expanded_cell_count = grand_expanded_cell_count + len(closed_list)
            print('    current_search_expanded_cell_count = ', str(len(closed_list)))
            print('    >> The agent followed the final search path and reached the goal position.')
            print('       ** total expanded cell count = (' + str(grand_expanded_cell_count) + '), from (' + str(counter) + ') searches.')
            print('       ** final grand_path length = ' + str(len(grand_path)))
            print('       ** final grand_path = ' + str(grand_path))
            break
        else:
            print('    hit a blocked cell; search again at position = ', str(agent_position))
            # append the path to grand_path
            for i in path: 
                if i != agent_position:
                    grand_path.append(i) 
                else:
                    break
            # collect expanded_cell_count
            grand_expanded_cell_count = grand_expanded_cell_count + len(closed_list)
        print('    current_search_expanded_cell_count = ', str(len(closed_list)))
        print('    grand_expanded_cell_count (collected so far) = ', grand_expanded_cell_count)
        # print('    grant_path (collected so far) = ', str(grand_path))
        start = agent_position

    # print the maze and path
    maze_print = deepcopy(maze)
    for i in range(len(maze_print)):
        for j in range(len(maze_print[i])):
            if maze_print[i][j] == 0:
                maze_print[i][j] = ' '
            elif maze_print[i][j] == 1:
                maze_print[i][j] = 'X'
    for path_position in grand_path:
        if maze_print[path_position[0]][path_position[1]] == ' ':
            maze_print[path_position[0]][path_position[1]] = '.'
    print()
    print ('>>> maze_print with path (output)')
    for i in range(len(maze_print)):
        for j in range(len(maze_print[i])):
            print(maze_print[i][j], end=' ')
        print()

if __name__ == '__main__':
    main()
