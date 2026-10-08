"""
Water Jug Search.

Three jugs (12, 8 and 3 gallons) and a faucet. Measure exactly 1 gallon.
Solved with BREADTH-FIRST-SEARCH as in Figure 3.9 of the textbook:

    function BREADTH-FIRST-SEARCH(problem) returns a solution node or failure
        node <- NODE(problem.INITIAL)
        if problem.IS-GOAL(node.STATE) then return node
        frontier <- a FIFO queue, with node as an element
        reached <- {problem.INITIAL}
        while not IS-EMPTY(frontier) do
            node <- POP(frontier)
            for each child in EXPAND(problem, node) do
                s <- child.STATE
                if problem.IS-GOAL(s) then return child
                if s is not in reached then
                    add s to reached
                    add child to frontier
        return failure

State:  a tuple with the gallons in each jug, e.g. (12, 0, 0)
"""

from collections import deque
 
# ---------------------------------------------------------------------------
# The problem (book section 3.1: INITIAL, ACTIONS, RESULT, IS-GOAL, ACTION-COST)
# ---------------------------------------------------------------------------
class WaterJugProblem:
    """The water jug problem as a search problem."""
 
    def __init__(self, capacities=(12, 8, 3), goal_amount=1):
        self.capacities = capacities              # size of each jug
        self.goal_amount = goal_amount            # gallons we want to measure
        self.initial = (0, 0, 0)                  # all three jugs start empty
 
    def actions(self, state):
        """All actions that change the state.
        ('fill', i)     fill jug i from the faucet
        ('empty', i)    empty jug i onto the ground
        ('pour', i, j)  pour jug i into jug j
        """
        actions = []
        for i in range(len(state)):
            if state[i] < self.capacities[i]:     # jug i is not full
                actions.append(("fill", i))
            if state[i] > 0:                      # jug i is not empty
                actions.append(("empty", i))
                for j in range(len(state)):
                    if j != i and state[j] < self.capacities[j]:   # j has room
                        actions.append(("pour", i, j))
        return actions
 
    def result(self, state, action):
        """Transition model: the state after doing the action."""
        jugs = list(state)
        if action[0] == "fill":
            i = action[1]
            jugs[i] = self.capacities[i]
        elif action[0] == "empty":
            i = action[1]
            jugs[i] = 0
        elif action[0] == "pour":
            i, j = action[1], action[2]
            room = self.capacities[j] - jugs[j]   # space left in jug j
            amount = min(jugs[i], room)           # pour until i empty or j full
            jugs[i] -= amount
            jugs[j] += amount
        return tuple(jugs)
 
    def is_goal(self, state):
        """Goal: any jug holds exactly the goal amount."""
        for amount in state:
            if amount == self.goal_amount:
                return True
        return False
 
    def action_cost(self, state, action, new_state):
        """Every action costs 1. ACTION-COST(s, a, s′) - the cost of doing action a in state s to reach state s′"""
        return 1
 
    def describe(self, action):
        """Readable text for an action, e.g. It changes ("pour", 0, 2) into 'Pour 12 -> 3'."""
        c = self.capacities
        if action[0] == "fill":
            return f"Fill {c[action[1]]}"
        if action[0] == "empty":
            return f"Empty {c[action[1]]}"
        return f"Pour {c[action[1]]} -> {c[action[2]]}"
 
 
# ---------------------------------------------------------------------------
# Search tree nodes (book section 3.3.2, "Search data structures")
# ---------------------------------------------------------------------------
class Node:
    """A node in the search tree."""
 
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent          # the node this one came from
        self.action = action          # the action that led here
        self.path_cost = path_cost    # cost from the start (here: number of steps)
 
 
def expand(problem, node):
    """EXPAND (Figure 3.7): generate the child nodes of node."""
    s = node.state
    children = []
    for action in problem.actions(s):
        s2 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s2)
        children.append(Node(state=s2, parent=node, action=action, path_cost=cost))
    return children
 
 
def solution_path(node):
    """Follow the parent links back to the start. Returns the list of nodes
    from the initial state to this node."""
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()
    return path
 
 
# ---------------------------------------------------------------------------
# Breadth-first search (Figure 3.9)
# ---------------------------------------------------------------------------
def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node
    frontier = deque([node])              # FIFO queue
    reached = {problem.initial}           # states already seen
    while frontier:                       # while not IS-EMPTY(frontier)
        node = frontier.popleft()         # POP: take from the front
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):        # early goal test
                return child
            if s not in reached:
                reached.add(s)
                frontier.append(child)    # add to the back
    return None                           # failure: no solution
 
 
# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
def main():
    problem = WaterJugProblem(capacities=(12, 8, 3), goal_amount=1)
    goal_node = breadth_first_search(problem)
 
    if goal_node is None:
        print("No solution found.")
        return
 
    print(f"Jugs {problem.capacities}, goal: exactly {problem.goal_amount} gallon\n")
    for step, node in enumerate(solution_path(goal_node)):
        if node.action is None:
            print(f"Start:                 {node.state}")
        else:
            print(f"Step {step}: {problem.describe(node.action):15} {node.state}")
    print(f"\nSolved in {goal_node.path_cost} steps.")
 
 
if __name__ == "__main__":
    main()