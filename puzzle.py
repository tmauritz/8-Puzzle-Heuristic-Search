import numpy as np

class Node:
    """a state of the puzzle during the solving process"""
    def __init__(self, state, action, parent):
        self.state = state
        self.action = action
        self.parent = parent
    def printboard(self):
        for row in self.state:
            print(row)

    def generate_child(self):
        return Node(self.state, self.action, self)

class Puzzle:
    def __init__(self, start):
        """Initializes the puzzle with the given starting state"""
        self.open = []          # States that have not been fully explored yet
        self.closed = []        # states that have been fully explored
        self.start = start      # starting state
        self.goal = [[0,1,2],[3,4,5],[6,7,8]]
        print("Puzzle initialized.\nStarting state: ")
        for row in start:
            print(row)
        print("Goal state: ")
        for row in self.goal:
            print(row)
        print("Current hamming distance: ", self.h_hamming())
        print("Current manhattan distance: ", self.h_manhattan())

    def solve(self):
        """Solves the puzzle"""
        print("Solving puzzle...")

    def f(self, start, goal):
        """Calculates the heuristic function: f(x) = h(x) + g(x)"""
        return 2

    def h_manhattan(self):
        """Calculates estimated cost of path from node to the goal (manhattan distance)"""
        # map the tile values to their positions in the goal state
        goal_positions = {}
        for row in range(len(self.goal)):
            for col in range(len(self.goal[row])):
                goal_positions[self.goal[row][col]] = (row, col)

        # calculate manhattan distance
        manhattan = 0
        for row in range(len(self.start)):
            for col in range(len(self.start[row])):
                tile = self.start[row][col]
                if tile != 0:  # Ignore the blank tile
                    goal_row, goal_col = goal_positions[tile]
                    # distance = |current row - goal row| + |current col - goal col|
                    manhattan += abs(row - goal_row) + abs(col - goal_col)
        return manhattan

    def g(self):
        """Calculates the cost of the solution so far (path from start node to current node"""
        return 1

    def h_hamming(self):
        """Calculates estimated cost of path from node to the goal (hamming distance)"""
        hamming = 0
        for x in range(3):
            for y in range(3):
                if self.start[x][y] != 0 and self.goal[x][y] != self.start[x][y]:
                    hamming += 1
        return hamming


def main():
    print("Welcome to puzzle heuristic")
    start = [[0,1,2],[3,4,5],[6,7,8]]
    puzzle = Puzzle(start)

if __name__ == '__main__':
    main()
