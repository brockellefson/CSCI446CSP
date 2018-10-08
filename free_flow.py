from collections import deque
import heapq
import mazes


class Search:
    def __init__(self, maze):
        self.px = 0
        self.py = 0
        self.fx = 0
        self.fy = 0
        self.maze = maze


if __name__=='__main__':
    #create mazes
    maze_5x5 = mazes.read_maze("5x5maze.txt")
    maze_7x7 = mazes.read_maze("7x7maze.txt")
    maze_8x8 = mazes.read_maze("8x8maze.txt")
    maze_9x9 = mazes.read_maze("9x9maze.txt")
