import heapq
import math

#global variables: start state, end state, obstacles list, tree, open list, closed list, search, g, h, n - the size of the maze
#no array for cost since it is always one
#store each state as a tuple such as (1,0)
#functions: h, actions, successor
#possible actions: 'l','r','u','d'

########### THIS is not complete - anything that is in comments, if it is not explaining a line of code, needs to be turned into code

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

start_state=(0,0)
goal_state=(0,0)
# obstacle_states=[]
#tree
open_list=[]
closed_list=[]
search=[]
g=[]
n=0
counter=0

def succ(s,a):
    if (a=='r'):
        return (s[0]+1,s[1])
    elif (a=='u'):
        return (s[0],s[1]+1)
    elif(a=='l'):
        return (s[0]-1,s[1])
    elif (a=='d'):
        return (s[0],s[1]-1)
    return 'error'

def actions(s):
    action=[]
    if (s[0]>0):
        action.append('l')
    if (s[0]<n-1):
        action.append('r')
    if (s[1]>0):
        action.append('u')
    if (s[1]<n-1):
        action.append('d')
    return action

def h(s):
    return abs(goal_state[0]-s[0])+abs(goal_state[1]-s[1])

def min():
    for item,index in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
    return current_index

def a_star():
    global start_state
    global goal_state
    # global obstacle_states
    global open_list
    global closed_list
    global search
    global counter
    global g
    prev_state=start_state
    while (g[goal_state[0]][goal_state[1]]>min()):
        state=open_list[min()]
        open_list.remove(min())
        closed_list=closed_list.append(state[1])
        for a in actions(state):
            next_state=succ(state,a)
            if (search[next_state[0]][next_state[1]]<counter):
                g[next_state[0]][next_state[1]]=math.inf
                search[next_state[0]][next_state[1]]=counter
            if (g[next_state[0]][next_state[1]]>g[state[0]][state[1]]+1):
                g[next_state[0]][next_state[1]]=g[state[0]][state[1]]+1
                node=Node(prev_state,state)
                prev_state=state
                #if next_state is in open_list then remove it from open
                #if next_state is not in obstacle_states, insert next_state into open_list with new f value


def main():
    global start_state
    global goal_state
    # global obstacle_states
    global open_list
    global closed_list
    global search
    global g
    global counter
    search = [[0 for i in range(n)] for j in range(n)] #initializes 2d array representing states to all be 0
    g=[[-1 for i in range(n)] for j in range(n)] #initializes all g values to be -1
    while (start_state!=goal_state):
        counter=counter+1
        g[start_state[0]][start_state[1]]=0
        search[start_state[0]][start_state[1]]=counter
        g[goal_state[0]][goal_state[1]]=math.inf
        search[goal_state[0]][goal_state[1]]=counter
        open_list=[]
        closed_list=[]
        start_node = Node(None, start_state)
        end_node = Node(None, goal_state)

        # if statement here to make check if the start_state is terrain or not
        if(g[start_state[0][start_state[1]]] == 'b'):
            print("terrain")
            closed_list.append()
            continue

        open_list.append((g[start_state[0]][start_state[0]]+h((start_state[0],start_state[1])),(start_state[0],start_state[1])))
        a_star()
        if (open_list==[]):
            print("I cannot reach the target")
            return
        #follow tree pointers
        #set s_start to current state
        #record any new obstacles in obstacle_states
    print("I reached the target")

