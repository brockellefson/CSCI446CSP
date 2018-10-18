from collections import defaultdict
import heapq
import mazes
import random


class CSP:
    def __init__(self, maze, debug):
        self.domain = []
        self.finish = {}
        self.start = {}
        self.visited = []
        self.color_visited = defaultdict(list)
        self.finish_path = defaultdict(list)
        self.island = []
        self.complete_colors = []
        self.debug = debug
        self.find_s_and_f(maze)
        mazes.print_maze(maze)


    def find_s_and_f(self, maze): #find start and finish to each color
        for row in maze:
            for node in row:
                if node.value is not '_':
                    self.visited.append(node) #append to visited so their values do not change
                    if node.value not in self.domain:
                        self.domain.append(node.value)
                    if node.value not in self.start:
                        self.start[node.value] = node
                        self.color_visited[node.value].append(node)
                    else:
                        self.finish[node.value] = node
                        self.color_visited[node.value].append(node)

    def dumb_backtracking(self, assignment):
        if self.complete(assignment): #if the assignment is complete, return and print maze
            mazes.print_maze(assignment)
            return assignment

        node = self.get_node(assignment) #get a node that has not been visited

        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False

        for color in self.get_colors(node):

            if self.debug:
                print("Evaluating: ")
                print("Domain is :{}".format(self.get_colors(node)))
                print("node is at x: {} y:{}".format(node.x, node.y))
                print("islands are: {}\ncomplete are: {}".format(self.island, self.complete_colors))
                node.value = 'X'
                mazes.print_maze(assignment)
                node.value = '_'

            if self.consistant(color, node, assignment): #if the color we have chosen is legal, use it
                self.visited.append(node)
                self.color_visited[color].append(node)

                result = self.dumb_backtracking(assignment) #move on to next node
                if result:
                    return result

                self.visited.remove(node) #that branch failed, backtrack
                self.color_visited[color].remove(node)
                if color in self.complete_colors:
                    self.complete_colors.remove(color)

                node.value = '_'
        return False

    def backtracking(self, assignment):
        pass

    def get_colors(self, node):
        colors = [] #prioitizes adjacent colors
        for neighbor in node.neighbors:
            if neighbor.value is not '_' and neighbor.value not in colors and neighbor.value not in self.complete_colors:
                colors.append(neighbor.value)
        for color in self.domain:
            if color not in colors and color not in self.complete_colors:
                colors.append(color)
        return colors

    def get_node(self, assignment):
        for row in assignment:
            for node in row:
                if node not in self.visited: #if node is not visited, return
                    return node

    def complete(self, assignment): #checks to see if assignment is correct
        for color in self.domain:
            if color not in self.complete_colors:
                return False
        print('Complete')
        return True

    def consistant(self, color, node, assignment):
        node.value = color

        #if the node will not cause a zig_zag, the start and finish node only have one child, and we dont corner any other nodes, move on
        for neighbor in node.neighbors:
            if neighbor.value is not '_':
                if self.zig_zag(neighbor, color) or not self.start_finish_cons(neighbor, color) or self.cornered(neighbor) or not self.color_partcomplete_start(neighbor.value) or not self.color_partcomplete_finish(neighbor.value):
                    node.value = '_'
                    return False

        local_complete, path = self.color_complete(color)
        if local_complete:
            self.finish_path[color] = path
            self.complete_colors.append(color)

        return True

    def zig_zag(self, node, color):
        if node.value is color:
            count = 0
            for neighbor in node.neighbors:
                if neighbor.value is color:
                    count += 1
                if count > 2:
                    return True
        return False

    def start_finish_cons(self, node, color):
        if node is self.start[color] or node is self.finish[color]:
            count = 0
            for neighbor in node.neighbors:
                if neighbor.value is color:
                    count += 1
                if count >= 2:
                    return False
        return True

    def cornered(self, node):
        for neighbor in node.neighbors: #if this node has no path to either a color or '_'
            if neighbor.value is '_' or neighbor.value is node.value:
                return False
        return True

    def color_complete(self, color):
        node = self.start[color]#checks to see if color is complete
        path = []
        while node is not self.finish[color]:
            for neighbor in node.neighbors:
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break
                elif neighbor is node.neighbors[-1]:
                    return False, path
        path.append(node)
        return True, path

    def color_partcomplete_start(self, color):
        node = self.start[color] #checks to see if color is part complete
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.finish[color] or neighbor.value is '_':
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    return False
        return False

    def color_partcomplete_finish(self, color):
        node = self.finish[color] #checks to see if color is part complete
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.start[color] or neighbor.value is '_':
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    return False
        return False

if __name__=='__main__':
    #create mazes
    maze_test = mazes.read_maze("5x5maze_solution.txt")
    maze_5x5 = mazes.read_maze("5x5maze.txt")
    maze_7x7 = mazes.read_maze("7x7maze.txt")
    maze_8x8 = mazes.read_maze("8x8maze.txt")
    maze_9x9 = mazes.read_maze("9x9maze.txt")
    maze_10x10 = mazes.read_maze("10x10maze.txt")
    maze_12x12 = mazes.read_maze("12x12maze.txt")
    maze_14x14 = mazes.read_maze("14x14maze.txt")

    print("Solving 5x5:")
    csp_5x5 = CSP(maze_5x5, False)
    csp_5x5.dumb_backtracking(maze_5x5)

    print("Solving 7x7:")
    csp_7x7 = CSP(maze_7x7, False)
    csp_7x7.dumb_backtracking(maze_7x7)

    print("Solving 8x8:")
    csp_8x8 = CSP(maze_8x8, False)
    csp_8x8.dumb_backtracking(maze_8x8)

    print("Solving 9x9:")
    csp_9x9 = CSP(maze_9x9, False)
    csp_9x9.dumb_backtracking(maze_9x9)

    print("Solving 10x10:")
    csp_10x10 = CSP(maze_10x10, False)
    csp_10x10.dumb_backtracking(maze_10x10)

    print("Solving 12x12:")
    csp_12x12 = CSP(maze_12x12, True)
    csp_12x12.dumb_backtracking(maze_12x12)

    print("Solving 14x14:")
    csp_14x14 = CSP(maze_14x14, False)
    csp_14x14.dumb_backtracking(maze_14x14)
