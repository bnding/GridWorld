import sys

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# get current node's children list based on its valid actions 
# assuming actions to and from known blocked cells were elliminated  
def get_children(current_node, maze, block_tag, children):
    """get current node's children list based on its valid actions"""
    # Generate children
    children = []
    # check action override
    # left (0, -1); right (0, 1); up (-1, 0); down (1, 0)
    succ_position_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    state_action_code = maze[current_node.position[0]][current_node.position[1]][3]
    if state_action_code != -1: 
        # left (0, -1); right (0, 1); up (-1, 0); down (1, 0)
        # left (0: no, 1: yes); right (0: no, 1: yes); up (0: no, 1: yes); down (0: no, 1: yes)
        # 0 = 0-0-0-0; 1 = 0-0-0-1; 2 = 0-0-1-0; 3 = 0-0-1-1; 4 = 0-1-0-0
        # 5 = 0-1-0-0; 6 = 0-1-1-0; 7 = 0-1-1-1; 8 = 1-0-0-0; 9 = 1-0-0-1
        # 10 = 1-0-1-0; 11 = 1-0-1-1; 12 = 1-1-0-0; 13 = 1-1-0-1; 14 = 1-1-1-0
        # 15 = 1-1-1-1;
        if state_action_code == 0:
            succ_position_list = []        # 0-0-0-0
        elif state_action_code == 1:
            succ_position_list = [(1, 0)]
        elif state_action_code == 2: 
            succ_position_list = [(-1, 0)]
        elif state_action_code == 3:
            succ_position_list = [(-1, 0), (1, 0)]
        elif state_action_code == 4: 
            succ_position_list = [(0, 1)]
        elif state_action_code == 5: 
            succ_position_list = [(0, 1), (1, 0)]
        elif state_action_code == 6: 
            succ_position_list = [(0, 1), (-1, 0)]
        elif state_action_code == 7: 
            succ_position_list = [(0, 1), (-1, 0), (1, 0)]
        elif state_action_code == 8: 
            succ_position_list = [(0, -1)]
        elif state_action_code == 9: 
            succ_position_list = [(0, -1), (1, 0)]
        elif state_action_code == 10: 
            succ_position_list = [(0, -1), (-1, 0)]
        elif state_action_code == 11: 
            succ_position_list = [(0, -1), (-1, 0), (1, 0)]
        elif state_action_code == 12: 
            succ_position_list = [(0, -1), (0, 1)]
        elif state_action_code == 13: 
            succ_position_list = [(0, -1), (0, 1), (1, 0)]
        elif state_action_code == 14: 
            succ_position_list = [(0, -1), (0, 1), (-1, 0)]
        elif state_action_code == 15: 
            succ_position_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # calculate default actions
    # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
    for new_position in succ_position_list: # Adjacent squares

        # Get the node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure it is not the parent of the current_node
        if current_node.parent and (current_node.parent.position ==  node_position):
            continue

        # Make sure it is within range
        if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
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
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

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
                current_node = item
                current_index = index

        # Pop the current off the open list, add to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        children = get_children(current_node, maze, block_tag, children)

        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

        #     # Get node position
        #     node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        #     # Make sure it is within range
        #     if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
        #         continue

        #     # Make sure it is walkable terrain
        #     if maze[node_position[0]][node_position[1]][0] == block_tag:
        #         continue

        #     # Create a new node
        #     new_node = Node(current_node, node_position)

        #     # Append
        #     children.append(new_node)

        # if no children: set f() to infinity
        # if len(children) == 0:
        #     current_node.g = 9999
        #     current_node.f = current_node.g + current_node.h

        # Loop through the children
        # new_child_to_open_list = 0
        for child in children:
            # Child is on the closed list
            in_closed_list = 0
            for closed_child in closed_list:
                if child == closed_child:
                    in_closed_list = 1
                    break
            if in_closed_list == 1:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # check if the "child" is in the open list
            # "replace" if it is in and child.g < open_node.g
            in_open_list = 0
            for count, elem in enumerate(open_list):
                if child == elem:
                    in_open_list = 1
                    if child.g < elem.g:
                        open_list.pop(count)
                        open_list.append(child)
                        # new_child_to_open_list = 1
            if in_open_list == 1:
                continue                    

            open_list.append(child)
            # new_child_to_open_list = 1
        
        # if new_child_to_open_list == 0:
        #     current_node.g = 9999
        #     current_node.f = current_node.g + current_node.h

            # if maze[child.position[0]][child.position[1]][1] < counter:     # first encounter to child in this search 
            #     maze[child.position[0]][child.position[1]][1] = counter
            #     open_list.append(child)                                 
            # else:
            #     # check if "child" is in the open list
            #     # "replace" if it is in and child.g < open_node.g
            #     for count, elem in enumerate(open_list):
            #         if child == elem and child.g < elem.g:
            #             open_list.pop(count)
            #             open_list.append(child)

# move along the path, stop if hits the blocked cell: remove relevant actions on relevant states  
def move_agent_from_start_to_goal(maze_knowlege, start, end, path, block_tag):
    prior_position = path[0]
    for i in range(len(path)):
        if maze_knowlege[path[i][0]][path[i][1]][0] >= block_tag:
            # left (0, -1); right (0, 1); up (-1, 0); down (1, 0)
            # left (0:no, 1:yes); right (0:no, 1:yes); up (0:no, 1:yes); down (0:no, 1:yes)
            # 0 = 0-0-0-0; 1 = 0-0-0-1; 2 = 0-0-1-0; 3 = 0-0-1-1; 4 = 0-1-0-0
            # 5 = 0-1-0-0; 6 = 0-1-1-0; 7 = 0-1-1-1; 8 = 1-0-0-0; 9 = 1-0-0-1
            # 10 = 1-0-1-0; 11 = 1-0-1-1; 12 = 1-1-0-0; 13 = 1-1-0-1; 14 = 1-1-1-0
            # 15 = 1-1-1-1;
            maze_knowlege[path[i][0]][path[i][1]][0] = 2
            maze_knowlege[path[i][0]][path[i][1]][3] = 0
            if path[i][0] > 0:
                if maze_knowlege[path[i][0]-1][path[i][1]][3] in [-1]:
                    maze_knowlege[path[i][0]-1][path[i][1]][3] = 14
                elif maze_knowlege[path[i][0]-1][path[i][1]][3] in [1,3,5,7,9,11,13,15]:
                    maze_knowlege[path[i][0]-1][path[i][1]][3] = maze_knowlege[path[i][0]-1][path[i][1]][3] - 1
            if path[i][0] < (len(maze_knowlege) - 1):
                if maze_knowlege[path[i][0]+1][path[i][1]][3] in [-1]:
                    maze_knowlege[path[i][0]+1][path[i][1]][3] = 13
                elif maze_knowlege[path[i][0]+1][path[i][1]][3] in [2,3,6,7,10,11,14,15]:
                    maze_knowlege[path[i][0]+1][path[i][1]][3] = maze_knowlege[path[i][0]+1][path[i][1]][3] - 2
            if path[i][1] > 0:
                if maze_knowlege[path[i][0]][path[i][1]-1][3] in [-1]:
                    maze_knowlege[path[i][0]][path[i][1]-1][3] = 11
                elif maze_knowlege[path[i][0]][path[i][1]-1][3] in [4,5,6,7,12,13,14,15]:
                    maze_knowlege[path[i][0]][path[i][1]-1][3] = maze_knowlege[path[i][0]-1][path[i][1]][3] - 4
            if path[i][1] < (len(maze_knowlege[path[i][0]]) - 1):
                if maze_knowlege[path[i][0]][path[i][1]+1][3] in [-1]:
                    maze_knowlege[path[i][0]][path[i][1]+1][3] = 7
                elif maze_knowlege[path[i][0]][path[i][1]+1][3] in [8,9,10,11,12,13,14,15]:
                    maze_knowlege[path[i][0]][path[i][1]+1][3] = maze_knowlege[path[i][0]+1][path[i][1]][3] - 8
            break

        prior_position = path[i]

    return prior_position

counter =0

# Initialize both the open and closed list
open_list = []
closed_list = []

def main():
    counter = 0
    grand_path = []

    # Initialize both the open and closed list
    global open_list
    global closed_list

    open_list = []
    closed_list = []

    start = (0, 0)
    end = (7, 6)
    
    # maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

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

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    print()
    print ('>>> maze (input)')
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            print(maze[i][j], end=' ')
        print()

    # -------------------------------------------------------------------------
    # initialize maze_knowledge
    # -------------------------------------------------------------------------
    # ** maze_knowlege represents an "environment"
    #      with a knowledge base learned overtime 
    # ** Each cell has 4 values associated with it:
    #      [blocked(s), search(s), heuristic(s), actions(s)]
    #    1) blocked(s) = 
    #       0: not blocked, 1: blocked but not learned, 2: blocked and learned 
    #    2) search(s) = (0, 1, 2... "n-th" ...) 
    #       the state s is "encountered" in the n-th search 
    #    3) heuristic(s), used in A* adaptive, 
    #       -1: take the default manhattan distance, or 
    #       a better h(s) override from the A* adaptive implementation  
    #    4) actions(s)
    #       **idea: use a single number to represent 
    #               all possible valid action combinations from state s.
    #       -1: take the default actions in 4 directions if do-able
    #       0, 1, 2, ..., 15: 
    #           these 16 values represent all possible action combinations  
    #       ** move left (0, -1); right (0, 1); up (-1, 0); down (1, 0)
    #          (1) move left (0: no, 1: yes); 
    #          (2) move right (0: no, 1: yes); 
    #          (3) move up (0: no, 1: yes); 
    #          (4) move down (0: no, 1: yes)
    #       ** therefore the below 16 values represents all action combinations
    #          decode [actions(s)] = Left-Right-Up-Down
    #          0 = 0-0-0-0; 1 = 0-0-0-1; 2 = 0-0-1-0; 3 = 0-0-1-1; 
    #          4 = 0-1-0-0; 5 = 0-1-0-0; 6 = 0-1-1-0; 7 = 0-1-1-1; 
    #          8 = 1-0-0-0; 9 = 1-0-0-1; 10 = 1-0-1-0; 11 = 1-0-1-1; 
    #          12 = 1-1-0-0; 13 = 1-1-0-1; 14 = 1-1-1-0; 15 = 1-1-1-1;
    # -------------------------------------------------------------------------
    print()
    print ('>>> maze (initialized, with knowledge base)')
    maze_knowlege = maze
    for i in range(len(maze_knowlege)):
        for j in range(len(maze_knowlege[i])):
            maze_knowlege[i][j] = [maze_knowlege[i][j],0,-1,-1]
            print(maze_knowlege[i][j], end=' ')
        print()

    while start != end:
        counter = counter + 1

        # Create the start and end nodes
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        maze_knowlege[start_node.position[0]][start_node.position[1]][1]=counter    # search(s)

        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        maze_knowlege[end_node.position[0]][end_node.position[1]][1]=counter    # search(s)

        # Initialize both the open and closed lists
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        block_tag = 2
        path = astar(maze_knowlege, start_node, end_node, block_tag, counter)
        # if len(open_list) == 0:
        #     print('I cannot research the target.')
        #     exit()

        # print path >> after astar()
        print()
        print ('>>> invoke astar()')
        print('    counter = ' + str(counter) + '; result search path = ' + str(path))

        # print maze_knowledge >> after astar()
        # print ('print maze_knowledge >> after astar()')
        # for i in range(len(maze_knowlege)):
        #     for j in range(len(maze_knowlege[i])):
        #         print(maze_knowlege[i][j], end=' ')
        #     print()

        print('>>> move_agent_from_start_to_goal()')
        block_tag = 1
        if path:
            agent_position = move_agent_from_start_to_goal(maze_knowlege, start, end, path, block_tag)
        else:
            agent_position = start

        # print maze_knowledge >> after move_agent_from_start_to_goal()
        # print ('print maze_knowledge >> after move_agent_from_start_to_goal()')
        # for i in range(len(maze_knowlege)):
        #     for j in range(len(maze_knowlege[i])):
        #         print(maze_knowlege[i][j], end=' ')
        #     print()
        
        # block test: agent start position 
        # if agent_position == start:
        #     print('Agent start position cell is blocked.')
        #     break
        
        # goal test
        if agent_position == end:
            grand_path = grand_path + path
            print('    Agent followed the final search path and reached the goal position.')
            print('    final grand_path = ' + str(grand_path))
            break
        else:
            print('    hit blocked cell, re-search at position = ', str(agent_position))
            # collect path
            if path:
                for i in path : 
                    if i != agent_position:
                        grand_path.append(i) 
                    else:
                        break
            print('    grant_path (collected so far) = ', str(grand_path))
            start = agent_position
        
        start = agent_position

if __name__ == '__main__':
    main()
