from collections import deque
import heapq
import mazes


class CSP:
    def __init__(self, domain, maze):
        self.domain = domain
        self.maze = maze

        for color in self.domain:
            print("coloring {}".format(color))
            self.csp(color, None, None)

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
                        #remove color you want from list of other colors
                        print("Start is at x:{}, y:{} \n Finish is at x:{}, y{}".format(start.x, start.y, finish.x, finish.y))
                        mazes.print_maze(self.maze)
                        self.a_search(start, finish)
                        return

    def a_search(self, curr_node, finish):
        #create heap queue for priority
        queue = []
        visited_nodes = []
        heapq.heapify(queue)
        #variable to always give unique identifiers to (priority, node) tuple
        task = 0
        heapq.heappush(queue, (0, task, curr_node))
        task += 1
        cost = {curr_node : 0}

        while len(queue) > 0:
            node = heapq.heappop(queue)[2]
            if node in visited_nodes:
                continue
            if node == finish:
                self.color_path(finish)
                return True

            visited_nodes.append(node)
            for neighbor in node.neighbors:
                new_cost = cost[node] + self.manhattan_d(neighbor, node)
                if neighbor not in visited_nodes and self.are_different(neighbor, finish):
                    if neighbor not in cost or new_cost < cost[neighbor]:
                        neighbor.previous = node
                        cost[neighbor] = new_cost
                        p = self.manhattan_d(neighbor, finish) + new_cost
                        heapq.heappush(queue, (p, task, neighbor))
                        task += 1
                        #self.print_current(neighbor)
        print("Could Not Find Path")
        return False

    def manhattan_d(self, curr_node, node):
        return abs(curr_node.x - node.x) + abs(curr_node.y - node.y)

    def are_different(self, curr_node, finish):
        #return true if next node is a valid space
        if curr_node.value is "_" or curr_node.value is finish.value:
            return True
        return False

    def not_cornered(self, curr_node):
        #checks to see that if we move to a node neighboring another color, we do not corner it
        for neighbor in curr_node.neighbors:
            if neighbor is not curr_node:
                if neighbor.value is "_" or neighbor.value is curr_node.value:
                    return True
            return False

    def print_neighbor(self, node):
        #prints out where path currently is for debugging
        actual = node.value
        node.value = "X"
        mazes.print_maze(self.maze)
        node.value = actual

    def color_path(self, node):
        print("Solution Found:")
        color = node.value
        while node.previous is not None:
            node.value = color
            node = node.previous
        mazes.print_maze(self.maze)

if __name__=='__main__':
    #create mazes
    maze_5x5 = mazes.read_maze("5x5maze.txt")
    #maze_7x7 = mazes.read_maze("7x7maze.txt")
    #maze_8x8 = mazes.read_maze("8x8maze.txt")
    #maze_9x9 = mazes.read_maze("9x9maze.txt")

    csp_5x5 = CSP(["B", "R", "O", "Y", "G"], maze_5x5)
    #csp_7x7 = CSP(["B", "R", "O", "Y", "G"], maze_7x7)
    #csp_8x8 = CSP(["B", "R", "O", "Y", "G", "P", "Q"], maze_8x8)
    #csp_9x9 = CSP(["B", "R", "O", "Y", "G", "P", "Q", "D", "K"], maze_9x9)
