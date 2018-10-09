from collections import defaultdict
import heapq
import mazes
import random


class CSP:
    def __init__(self, domain, maze):
        self.domain = domain
        self.maze = maze
        self.moves = []
        self.color_queue = defaultdict(list)
        self.color_visited = defaultdict(list)
        self.color_finish = {}
        self.color_start = {}
        self.task = 0
        for color in self.domain:
            self.csp(color, None, None)
        mazes.print_maze(self.maze)
        self.greedy_search()

    def csp(self, color, start, finish):
        #find path for each color
        for row in self.maze:
            for element in row:
                if element.value is color:
                    if start is None:
                        start = element
                        continue
                    else:
                        #start has already been found, set next node of that color to finish
                        finish = element

                        #add finish to dic of colors finish
                        self.color_finish[color] = finish
                        self.color_start[color] = start

                        #add start to dic of that colors visited heap
                        heapq.heapify(self.color_queue[color])
                        heapq.heappush(self.color_queue[color], (0, self.call_task(), start))
                        return

    def greedy_search(self):
        color = 0
        curr_color = self.domain[color] #sets current color to track
        queue = self.color_queue[curr_color] #gives the first color from domains list of visited nodes, then picks first node visited

        #while there are still colors
        while color >= 0:
            #while there is still aval nodes
            while len(queue) > 0:
                    node = heapq.heappop(queue)[2] #pops node
                    print("Evaluating x:{} y:{}, current color is {} and is_visited is: {}".format(node.x, node.y, curr_color, self.in_visited(node)))
                    org_val = node.value
                    node.value = 'X'
                    mazes.print_maze(self.maze)
                    node.value = org_val

                    if node in self.color_visited.values():
                        continue

                    if node is self.color_finish[curr_color]:
                        print("Color {} found solution on node {} Coord: x:{} y{}".format(curr_color, node.value, node.x, node.y))
                        print ("The real solution is on x:{} y{}\n".format(self.color_finish[curr_color].x, self.color_finish[curr_color].y))
                        #advance to next color
                        color += 1
                        #if all colors are done, print maze
                        if color > len(self.domain) - 1:
                            self.color_path()
                            return True
                        curr_color = self.domain[color] #sets current color to track
                        queue = self.color_queue[curr_color] #gives the first color from domains list of visited nodes, then picks first node visited
                        continue

                    self.color_visited[curr_color].append(node)
                    for neighbor in node.neighbors:
                        if self.are_different(neighbor, self.color_finish[curr_color]):
                            if self.in_visited(neighbor):
                                continue

                            neighbor.previous = node
                            heapq.heappush(queue, (self.manhattan_d(neighbor, self.color_finish[curr_color]), self.call_task(), neighbor))
            print("Mistake made, backtracking")
            del self.color_visited[curr_color]
            color -= 1
            curr_color = self.domain[color] #sets current color to track
            queue = self.color_queue[curr_color] #gives the first color from domains list of visited nodes, then picks first node visited
        print("Solution Not Found")
        return False

    def call_task(self):
        self.task += 1
        return self.task

    def in_visited(self, curr_node):
        for visted_nodes in self.color_visited.values():
            if curr_node in visted_nodes:
                return True
        return False

    def manhattan_d(self, curr_node, node):
        return abs(curr_node.x - node.x) + abs(curr_node.y - node.y)

    def are_different(self, curr_node, finish):
        #return true if next node is a valid space
        if curr_node.value is "_" or curr_node.value is finish.value:
            return True
        return False

    def print_current(self, node):
        #prints out where path currently is for debugging
        actual = node.value
        node.value = "X"
        mazes.print_maze(self.maze)
        node.value = actual

    def color_path(self):
        print("Solution Found:")
        for color in self.domain:
            print ("Color {} Solution:".format(color))
            for node in self.color_visited[color]:
                node.value = color
            mazes.print_maze(self.maze)
            print("Length of visited stack for {}: {}".format(color, len(self.color_visited[color])))
            print("Node: {} x: {} y: {}".format(node.value, node.x, node.y))
if __name__=='__main__':
    #create mazes
    maze_5x5 = mazes.read_maze("5x5maze.txt")
    maze_7x7 = mazes.read_maze("7x7maze.txt")
    maze_8x8 = mazes.read_maze("8x8maze.txt")
    maze_9x9 = mazes.read_maze("9x9maze.txt")

    csp_5x5 = CSP(["B", "R", "O", "Y", "G"], maze_5x5)
    csp_7x7 = CSP(["B", "R", "O", "Y", "G"], maze_7x7)
    csp_8x8 = CSP(["B", "R", "O", "Y", "G", "P", "Q"], maze_8x8)
    csp_9x9 = CSP(["B", "R", "O", "Y", "G", "P", "Q", "D", "K"], maze_9x9)
