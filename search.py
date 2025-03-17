# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    need_visit= util.Stack() # need_visit is a stack(LIFO) for saving all states needed to visit
    already_visited=[] # already_visited is a list for saving all states that we visited to reach certain state

    start=problem.getStartState() # get the start state from getStartState() function
    need_visit.push((start, [])) # push the start state and empty list of directions in stack

    while not need_visit.isEmpty(): # loop until all nodes are visited
        (node, direction) = need_visit.pop()

        if not node in already_visited:
            already_visited.append(node) # if the node is not visited yet, I will append it in already_visited.

            if problem.isGoalState(node): 
                return direction # if node is goalstate, I will return direction to reach this state
                break

            for successor_state, actions, cost in problem.getSuccessors(node):
                need_visit.push((successor_state, direction + [actions])) # I will push successor_state and updated direction to the stack
             
    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    need_visit=util.Queue() # need_visit is a queue(FIFO) for saving all states needed to visit
    already_visited=[] # already_visited is a list for saving all states that we visited to reach certain state

    start=problem.getStartState() # get the start state from getStartState() function
    need_visit.push((start, [])) # push the start state and empty list of directions in queue

    while not need_visit.isEmpty(): # loop until all nodes are visited
        (node, direction) = need_visit.pop()
        
        if not node in already_visited:
            already_visited.append(node) # if the node is not visited yet, I will append it in already_visited.

            if problem.isGoalState(node):
                return direction  #if node is goalstate, I will return direction to reach this state
                break

            for successor_state, actions, cost in problem.getSuccessors(node):
                need_visit.push((successor_state, direction + [actions])) # I will push successor_state and updated direction to the Queue

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    need_visit=util.PriorityQueue() # need_visit is a priority queue(considering cost) for saving all states needed to visit
    already_visited=[] # already_visited is a list for saving all states that we visited to reach certain state

    start=problem.getStartState() # get the start state from getStartState() function
    need_visit.push((start, [], 0), 0) # push the start state and cost of 0 to the priority queue

    while not need_visit.isEmpty():  # loop until all nodes are visited
        (node, direction, cost) = need_visit.pop()
        
        if not node in [x[0] for x in already_visited]:
            already_visited.append((node, cost)) # if the node is not visited yet, I will append node and cost in already_visited.

            if problem.isGoalState(node):
                return direction  #if node is goalstate, I will return direction to reach this state
                break

            for successor_state, actions, step_cost in problem.getSuccessors(node):
                total_cost=cost+step_cost # update the total cost to reach the successor
                need_visit.push((successor_state, direction+[actions], total_cost), total_cost)

        else: # if the node has been visited before
            if [x[1] for x in already_visited if x[0]==node][0]> cost: # check if the new path has lower cost than the previous cost
                for successor_state, actions, step_cost in problem.getSuccessors(node):
                    total_cost=cost+step_cost # update the total cost to reach the successor
                    need_visit.push((successor_state, direction+[actions], total_cost), total_cost)

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    need_visit=util.PriorityQueue()  # need_visit is a priority queue(considering cost) for saving all states needed to visit
    already_visited= set() # already_visited is a set for saving all states that we visited to reach certain state. 

    start=problem.getStartState() # get the start state from getStartState() function
    need_visit.push((start, [], 0), 0) # push the start state and  cost of 0 to the priority queue

    while not need_visit.isEmpty(): # loop until all nodes are visited
        (node, direction, cost) = need_visit.pop()

        if not node in already_visited:
            already_visited.add(node) # if the node is not visited yet, I will append node in already_visited.

            if problem.isGoalState(node):
                return direction #if node is goalstate, I will return direction to reach this state
                break

            for successor_state, actions, step_cost in problem.getSuccessors(node):
                total_cost=cost+step_cost # total cost to reach the successor
                new_direction = direction + [actions] # update direction with new actions
                heuristic_cost = total_cost + heuristic(successor_state, problem) # heuristic cost is sum of culmulative cost and estimated cost
                need_visit.push((successor_state, new_direction, total_cost), heuristic_cost)
        


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
