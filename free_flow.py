from collections import deque
import heapq
import mazes


class CSP:
    def __init__(self, domain, maze):
        self.domain = domain
        self.maze = maze

    def greedy_search(self, curr_node, finish):
        #create heap queue for priority
        queue = []
        visited_nodes = []
        heapq.heapify(queue)
        #variable to always give unique identifiers to (priority, node) tuple
        task = 0
        heapq.heappush(queue, (0, task, curr_node))
        task += 1

        while len(queue) > 0:
            node = heapq.heappop(queue)[2]

            if node.value == finish:
                mazes.print_maze(self.maze)
                return True

            moves += 1
            visited_nodes.append(node)
            for neighbor in node.neighbors:
                if neighbor not in visited_nodes and self.are_different(node, neighbor)
                    neighbor.previous = node

                    #hmmmmmmmmmmmm
                    #heapq.heappush(queue, (self.manhattan_d(neighbor, self.fx, self.fy), task, neighbor))
                    task += 1
        return False

    def manhattan_d(self, curr_node, node):
        return abs(curr_node.x - node.x) + abs(curr_node.y - node.y)


    def are_different(self, curr_node, node):
        #return true if next node is a valid space
        if node.value is curr_node.value or node.value is "_":
            return True
        return False

    def cornered(self, curr_node):
        #checks to see that if we move to a node neighboring another color, we do not corner it
        for neighbor in curr_node.neighbors:
            if neighbor.value is "_" or neighbor.value is curr_node.value:
                return True
            return False

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
