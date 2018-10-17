from collections import defaultdict
import heapq
import mazes
import random


class CSP:
    def __init__(self, domain, maze):
        self.domain = domain
        self.finish = {}
        self.start = {}
        self.visited = []
        self.complete_colors = []
        self.find_s_and_f(maze)
        mazes.print_maze(maze)


    def find_s_and_f(self, maze): #find start and finish to each color
        for row in maze:
            for node in row:
                if node.value is not '_':
                    self.visited.append(node) #append to visited so their values do not change
                    if node.value not in self.start:
                        self.start[node.value] = node
                    else:
                        self.finish[node.value] = node

    def dumb_backtracking(self, assignment):
        if self.complete(assignment): #if the assignment is complete, return and print maze
            mazes.print_maze(assignment)
            return assignment

        node = self.get_node(assignment) #get a node that has not been visited

        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False

        #print("Evaluating: ")
        #print("node is at x: {} y:{}".format(node.x, node.y))
        #mazes.print_maze(assignment)


        for color in self.get_colors(node):
            if self.consistant(color, node, assignment): #if the color we have chosen is legal, use it
                self.visited.append(node)
                result = self.dumb_backtracking(assignment) #move on to next node
                if result:
                    return result
                self.visited.remove(node) #that branch failed, backtrack
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
            if not self.complete_util(color, assignment): #if each color is complete, the assignment is complete
                return False
        print('Complete')
        return True

    def complete_util(self, color, assignment):
        node = assignment[self.start[color].x][self.start[color].y]
        path = []
        while node not in path: #for each neighbor at node, find the one with the same color as node, and traverse until finish is found
            for neighbor in node.neighbors:
                if neighbor is assignment[self.finish[color].x][self.finish[color].y]:
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break
                elif neighbor.value is '_' or neighbor is node.neighbors[-1]: #if finish is not found, the color is not complete
                    return False
        return False

    def consistant(self, color, node, assignment):
        node.value = color

        #for color in self.domain:
        #    if self.color_complete(color):
        #        if self.islands(color, assignment):
        #            node.value = '_'
        #            return False

        #if the node will not cause a zig_zag, the start and finish node only have one child, and we dont corner any other nodes, move on
        for neighbor in node.neighbors:
            if neighbor.value is not '_':
                if self.zig_zag(neighbor, color) or not self.start_finish_cons(neighbor, color) or self.cornered(neighbor) or not self.color_partcomplete_start(neighbor.value) or not self.color_partcomplete_finish(neighbor.value):
                    node.value = '_'
                    return False

        if self.color_complete(color):
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
        if not self.cornered_util(node):
            return True
        return False

    def cornered_util(self, node):
        for neighbor in node.neighbors: #if this node has no path to either a color or '_'
            if neighbor.value is '_' or neighbor.value is node.value:
                return True
        return False

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
                    return False
        return True

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

    def islands(self, color, assignment):
        pass

if __name__=='__main__':
    #create mazes
    maze_test = mazes.read_maze("5x5maze_solution.txt")
    maze_5x5 = mazes.read_maze("5x5maze.txt")
    maze_7x7 = mazes.read_maze("7x7maze.txt")
    maze_8x8 = mazes.read_maze("8x8maze.txt")
    maze_9x9 = mazes.read_maze("9x9maze.txt")
    maze_test = mazes.read_maze("5x5maze_solution.txt")


    #csp_test = CSP(["B", "R", "O", "Y", "G"], maze_test)

    #csp_5x5 = CSP(["B", "R", "O", "Y", "G"], maze_5x5)
    #csp_5x5.dumb_backtracking(maze_5x5)


    csp_7x7 = CSP(["B", "R", "O", "Y", "G"], maze_7x7)
    csp_7x7.dumb_backtracking(maze_7x7)

    #csp_8x8 = CSP(["B", "R", "O", "Y", "G", "P", "Q"], maze_8x8)

    #csp_9x9 = CSP(["B", "R", "O", "Y", "G", "P", "Q", "D", "K"], maze_9x9)
