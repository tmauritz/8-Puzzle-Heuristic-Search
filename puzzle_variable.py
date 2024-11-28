class Node:
    def __init__(self, data, level, f_value):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.parent = None
        self.data = data
        self.level = level
        self.f_value = f_value

    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up,down,left,right} """
        x, y = self.find(self.data, 0)
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up,down,left,right] respectively. """
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                child_node.parent = self
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move the blank space in the given direction and if the position value are out
            of limits the return None """
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def copy(self, root):
        """ Copy function to create a similar matrix of the given node"""
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find(self, puz, x):
        """ Finds the position of x in the matrix - used for finding the blank space """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j

class Puzzle:

    def __init__(self, heuristic):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.n = 3
        self.h = heuristic
        self.open = []
        self.closed = []
        self.nodes_explored = 0
        self.nodes_in_solution = 0

    def is_solvable(self):
        """ Check if the puzzle is solvable """

    def f(self, start, goal):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return self.h(start.data, goal) + start.level

    def process(self,start, goal):
        """ Accept Start and Goal Puzzle state"""
        prettyprint_matrix(start)
        start = Node(start, 0, 0)
        start.f_value = self.f(start, goal)
        """ Put the start node in the open list"""
        self.open.append(start)

        print("\nLooking for Solution..\n")

        while True:
            self.nodes_explored=self.nodes_explored+1
            else: print(".", end="")
            cur = self.open[0]
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if self.h(cur.data, goal) == 0:
                print("Solution found:")
                self.print_solution(cur)
                break
            for i in cur.generate_child():
                i.f_value = self.f(i, goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]
            """ sort the open list based on f value """
            self.open.sort(key=lambda x: x.f_value, reverse=False)
        print("No solution found.\n")

    def print_solution(self,node):
        if node.parent is not None:
            self.print_solution(node.parent)
        print("----------")
        prettyprint_matrix(node.data)
        self.nodes_explored=self.nodes_explored+1


def prettyprint_matrix(matrix):
    for i in matrix:
        for j in i:
            print(j, end=" ")
        print("")


def h_manhattan(start, goal):
    """Calculates estimated cost of path from node to the goal (manhattan distance)"""
    # map the tile values to their positions in the goal state
    goal_positions = {}
    for row in range(len(goal)):
        for col in range(len(goal[row])):
            goal_positions[goal[row][col]] = (row, col)
    # calculate manhattan distance
    manhattan = 0
    for row in range(len(start)):
        for col in range(len(start[row])):
            tile = start[row][col]
            if tile != 0:  # Ignore the blank tile
                goal_row, goal_col = goal_positions[tile]
                # distance = |current row - goal row| + |current col - goal col|
                manhattan += abs(row - goal_row) + abs(col - goal_col)
    return manhattan

def h_hamming(start, goal):
    """Calculates estimated cost of path from node to the goal (hamming distance)"""
    hamming = 0
    for x in range(3):
        for y in range(3):
            if start[x][y] != 0 and goal[x][y] != start[x][y]:
                hamming += 1
    return hamming

if __name__ == '__main__':
    puzzlestart = [[1, 8, 2],
             [3, 4, 5],
             [6, 7, 0]]
    puzzlegoal = [[0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]]

    puzzle = Puzzle(h_manhattan)
    puzzle.process(puzzlestart, puzzlegoal)