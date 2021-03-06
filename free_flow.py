from collections import defaultdict
import heapq
import mazes
import random
import constraints
import sys
import time

class CSP:
    def __init__(self, maze, debug):
        self.domain = []
        self.finish = {}
        self.start = {}
        self.visited = []
        self.complete_colors = []
        self.debug = ''
        if debug is 'True':
            self.debug = True
        elif debug is 'False':
            self.debug = False
        self.moves = 0
        self.find_s_and_f(maze)
        print('Solving:')
        mazes.print_maze(maze)
        self.c = constraints.Constraints(self.start, self.finish, self.debug)




    def find_s_and_f(self, maze): #find start and finish source to each color
        for row in maze:
            for node in row:
                if node.value is not '_':
                    self.visited.append(node) #append to visited so their values do not change
                    if node.value not in self.domain:
                        self.domain.append(node.value)
                    if node.value not in self.start:
                        self.start[node.value] = node
                    else:
                        self.finish[node.value] = node

    def dumb_backtracking(self, assignment): #backtracking with no heuristics
        if self.complete(assignment): #if the assignment is complete, return and print maze
            mazes.print_maze(assignment)
            return assignment

        node = self.get_node(assignment) #get a node that has not been visited

        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False
        for color in self.get_colors(node): #get all colors that are not complete
            self.moves += 1
            if self.debug:
                print("Evaluating: ")
                print("Domain is :{}".format(self.get_colors(node)))
                print("Color: {}".format(color))
                print("node is at x: {} y:{}".format(node.x, node.y))
                node.value = 'X'
                mazes.print_maze(assignment)
                node.value = '_'

            if self.consistant(color, node, assignment): #if the color we have chosen is legal, use it
                if self.color_complete(color):
                    self.complete_colors.append(color)
                self.visited.append(node)

                result = self.dumb_backtracking(assignment) #move on to next node
                if result:
                    return result

                self.visited.remove(node) #that branch failed, backtrack
                if color in self.complete_colors:
                    self.complete_colors.remove(color)

                node.value = '_'
        return False

    def backtracking(self, assignment): #backtracking with heuristics
        if self.complete(assignment): #if the assignment is complete, return and print maze
            mazes.print_maze(assignment)
            return assignment

        colors, node = self.get_min_rem_val(assignment) #get a node that has the least amount of available legal moves

        if node is None: #when all nodes have been visited but the assignment is not complete, instant fail
            return False

        for color in colors:
            self.moves += 1
            if self.debug:
                print("Evaluating: ")
                print("Domain is :{}".format(self.get_colors(node)))
                print("Color: {}".format(color))
                print("node is at x: {} y:{}".format(node.x, node.y))
                node.value = 'X'
                mazes.print_maze(assignment)
                node.value = '_'

            node.value = color
            self.visited.append(node)

            if self.color_complete(color):
                self.complete_colors.append(color)

            result = self.backtracking(assignment) #move on to next node
            if result:
                return result

            self.visited.remove(node) #that branch failed, backtrack
            if color in self.complete_colors:
                self.complete_colors.remove(color)

            node.value = '_'
        return False

    def get_min_rem_val(self, assignment): #find node with least available legal colors
        variable_values = []
        id = 1 #for unique ID's to break tie breakers
        heapq.heapify(variable_values)
        for row in assignment:
            for node in row:
                if node not in self.visited:
                    legal_colors = []
                    for color in self.domain:
                        if color not in self.complete_colors:
                            if self.consistant(color, node, assignment):
                                node.value = '_'
                                legal_colors.append(color)
                    if len(legal_colors) is 1:
                        return legal_colors, node
                    else:
                        heapq.heappush(variable_values, (len(legal_colors), id, legal_colors, node))
                        id += 1

        curr_node = heapq.heappop(variable_values)
        return curr_node[2], curr_node[3]

    def get_colors(self, node): #get a color that is not complete
        colors = [] #prioitizes adjacent colors
        for neighbor in node.neighbors:
            if neighbor.value is not '_' and neighbor.value not in colors and neighbor.value not in self.complete_colors:
                colors.append(neighbor.value)
        for color in self.domain:
            if color not in colors and color not in self.complete_colors:
                colors.append(color)
        return colors

    def get_node(self, assignment): #get a node that is not visited
        for row in assignment:
            for node in row:
                if node not in self.visited: #if node is not visited, return
                    return node

    def complete(self, assignment): #checks to see if assignment is correct
        for color in self.domain:
            if color not in self.complete_colors:
                return False
        print('Complete')
        print('Total Assignments: {}'.format(self.moves))
        return True

    def color_complete(self, color): #checks to see if color is complete
        node = self.start[color]
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

    def consistant(self, color, node, assignment): #checks to see that color will not violate any constraints
        node.value = color

        #if the node will not cause a zig_zag, the start and finish node only have one child, and we dont corner any other nodes, move on
        for neighbor in node.neighbors:
            if neighbor.value is not '_':
                if self.c.zig_zag(neighbor, color) or self.c.cornered(neighbor) or not self.c.color_partcomplete_start(neighbor.value) or not self.c.color_partcomplete_finish(neighbor.value):
                    node.value = '_'
                    return False
        return True

if __name__=='__main__':
    dumb_maze = mazes.read_maze(sys.argv[1])
    csp_dumb = CSP(dumb_maze, sys.argv[2])
    start = time.time()
    csp_dumb.dumb_backtracking(dumb_maze)
    end = time.time()
    print("Dumb search took {} seconds\n".format(end - start))


    smart_maze = mazes.read_maze(sys.argv[1])
    csp_smart = CSP(smart_maze, sys.argv[2])
    start = time.time()
    csp_smart.backtracking(smart_maze)
    end = time.time()
    print("Smart search took {} seconds\n".format(end - start))
