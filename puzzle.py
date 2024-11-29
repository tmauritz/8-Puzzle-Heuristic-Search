GOAL = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def copy(root):
    """ Copy function to create a similar matrix of the given node"""
    temp = []
    for i in root:
        t = []
        for j in i:
            t.append(j)
        temp.append(t)
    return temp


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
            temp_puz = copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def find(self, puz, x):
        """ Finds the position of x in the matrix - used for finding the blank space """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j

    def equals(self, other_node):
        """ Compares two nodes based on their matrix """
        for x in range(0, len(self.data)):
            for y in range(0, len(self.data)):
                if self.data[x][y] != other_node.data[x][y]:
                    return False
        return True

class Puzzle:

    def __init__(self, heuristic):
        """ Initialize the puzzle size by the specified size,open and closed lists to empty """
        self.n = 3
        self.h = heuristic
        self.open = []
        self.closed = []
        self.nodes_explored = 0
        self.nodes_in_solution = 0
        self.solution_node = None

    def f(self, start, goal):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return self.h(start.data, goal) + start.level

    def find_solution(self, start, goal):
        """Attempts to find a solution to the puzzle"""
        self.nodes_explored = 0
        self.nodes_in_solution = 0
        """ Accept Start and Goal Puzzle state"""
        start = Node(start, 0, 0)
        start.f_value = self.f(start, goal)
        """ Put the start node in the open list"""
        self.open.append(start)

        print("\nLooking for solution... ")

        while len(self.open) > 0:
            self.nodes_explored=self.nodes_explored+1
            current_node = self.open[0]
            print("\r Node", self.nodes_explored, "Distance:", self.h(current_node.data, GOAL), "F-Value:",current_node.f_value, end="")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if self.h(current_node.data, goal) == 0:
                print("Solution found!")
                self.solution_node = current_node
                self.process_solution(current_node)
                return
            for node_child in current_node.generate_child():
                unique_child = True
                for closed_node in self.closed:
                    if closed_node.equals(node_child): unique_child = False
                if unique_child:
                    node_child.f_value = self.f(node_child, goal)         # calculate new f value for child
                    self.open.append(node_child)
            self.closed.append(current_node)
            del self.open[0]
            """ sort the open list based on f value """
            self.open.sort(key=lambda x: x.f_value, reverse=False)
        print("No solution found.")

    def process_solution(self, node, print_solution=False):
        """Prints the solution path to the console and counts the steps needed to solve the puzzle"""
        step = self.nodes_in_solution
        if node.parent is not None:
            self.nodes_in_solution = self.nodes_in_solution + 1
            self.process_solution(node.parent)
        else:
            if print_solution: print("Steps to Solution:")
        if print_solution:
            print("---------",step, "moves from goal")
            prettyprint_matrix(node.data)

def is_solvable(matrix):
    """ Checks if the puzzle is solvable """
    flat_matrix = flatten_matrix(matrix)
    inversions = 0
    empty_value = -1
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if flat_matrix[j] != empty_value and flat_matrix[i] != empty_value and flat_matrix[i] > flat_matrix[j]:
                inversions += 1
    return inversions%2==0

def prettyprint_matrix(matrix):
    """Prints the 3x3 matrix to the console"""
    for i in matrix:
        for j in i:
            print(j, end=" ")
        print("")

def flatten_matrix(matrix):
    """Flattens the given 3x3 matrix into a list"""
    return [item for sub_list in matrix for item in sub_list]

def list_to_matrix(list):
    """Transforms a list of 9 items into a 3x3 matrix (for longer lists the elements after will be truncated"""
    return [list[:3], list[3:6], list[6:]]

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

def main():
    """ main function with examples """
    puzzlestart = [[5, 2, 0], [8, 4, 3], [1, 7, 6]]
    #[[5, 2, 0], [8, 4, 3], [1, 7, 6]]
    #[[1, 8, 2],[3, 4, 5],[6, 7, 0]]

    print(is_solvable(puzzlestart))
    print(flatten_matrix(puzzlestart))
    print(list_to_matrix(flatten_matrix(puzzlestart)))
    print("Manhattan", h_manhattan(puzzlestart, GOAL))
    print("Hamming", h_hamming(puzzlestart, GOAL))

    puzzle = Puzzle(h_manhattan)
    puzzle.find_solution(puzzlestart, GOAL)
    print("Nodes explored: ", puzzle.nodes_explored)
    print("Nodes in_solution: ", puzzle.nodes_in_solution)


if __name__ == '__main__':
    main()
