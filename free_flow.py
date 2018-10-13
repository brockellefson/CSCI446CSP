from collections import defaultdict
import heapq
import mazes
import random


class CSP:
    def __init__(self, domain, maze):
        self.domain = domain
        self.finish = {}
        self.start = {}
        self.find_s_and_f(maze)
        mazes.print_maze(maze)

    def find_s_and_f(self, maze):
        #find path for each color
        for row in maze:
            for node in row:
                if node.value is not '_':
                    if node.value not in self.start:
                        self.start[node.value] = node
                    else:
                        self.finish[node.value] = node

    def dumb_backtracking(self, assignment):
        self.dumb_backtracking_util([])

    def dumb_backtracking_util(self, assignment):
        pass

    def backtracking(self, assignment):
        self.backtracking_util([])

    def backtracking_util(self, assignment):
        pass

    def complete(self, assignment):
        for color in self.domain:
            if not self.complete_util(color):
                return False
        return True

    def complete_util(self, color):
        node = self.start[color]
        while node.visited is False:
            for neighbor in node.neighbors:
                if neighbor.value is color and not neighbor.visited:
                    if neighbor is self.finish[color]:
                        return True
                    node.is_visited()
                    node = neighbor
                    break
                elif neighbor.value is '_' or neighbor is node.neighbors[-1]:
                    return False
        return False

if __name__=='__main__':
    #create mazes
    maze_5x5 = mazes.read_maze("5x5maze.txt")
    #maze_7x7 = mazes.read_maze("7x7maze.txt")
    #maze_8x8 = mazes.read_maze("8x8maze.txt")
    #maze_9x9 = mazes.read_maze("9x9maze.txt")
    maze_test = mazes.read_maze("5x5maze_solution.txt")


    csp_test = CSP(["B", "R", "O", "Y", "G"], maze_test)
    csp_5x5 = CSP(["B", "R", "O", "Y", "G"], maze_5x5)

    csp_test.start.clear()
    csp_test.finish.clear()

    for color in csp_test.domain:
        csp_test.start[color] = maze_test[csp_5x5.start[color].x][csp_5x5.start[color].y]
        csp_test.finish[color] = maze_test[csp_5x5.finish[color].x][csp_5x5.finish[color].y]

    print("The test is complete: {}".format(csp_test.complete(maze_test)))

    #csp_7x7 = CSP(["B", "R", "O", "Y", "G"], maze_7x7)
    #csp_8x8 = CSP(["B", "R", "O", "Y", "G", "P", "Q"], maze_8x8)
    #csp_9x9 = CSP(["B", "R", "O", "Y", "G", "P", "Q", "D", "K"], maze_9x9)
