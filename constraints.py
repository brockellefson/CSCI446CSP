class Constraints:

    def __init__(self, start, finish, debug):
        self.start = start
        self.finish = finish
        self.debug = debug

    def zig_zag(self, node, color): #checks to see that no adjacent nodes are zig_zaging
        if node.value is color:
            count = 0
            for neighbor in node.neighbors:
                if neighbor.value is color:
                    count += 1

                if node is self.start[color] or node is self.finish[color]:
                    if count >= 2:
                        if self.debug:
                            print("Failed due to zig_zag source")
                        return True

                elif count > 2:
                    if self.debug:
                        print("Failed due to zig_zag non source")
                    return True
        return False

    def cornered(self, node): #checks to see that node is not cornered
        color = node.value

        if node is self.finish[color] or node is self.start[color]:
            return False

        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.finish[color] or neighbor is self.start[color]:
                    return False
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    for neighbor in node.neighbors:
                        if neighbor.value is '_':
                            return False
                    if self.debug:
                        print("Failed due to cornered")
                    return True
        if self.debug:
            print("Failed due to cornered")
        return True

    def color_partcomplete_start(self, color): #checks to see if color is part complete
        node = self.start[color]
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.finish[color]:
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    for neighbor in node.neighbors:
                        if neighbor.value is '_':
                            return True
                    if self.debug:
                        print("Failed due to part complete start on color: {}".format(color))
                    return False
        if self.debug:
            print("Failed due to part complete start on color: {}".format(color))
        return False

    def color_partcomplete_finish(self, color): #checks to see if color is part complete
        node = self.finish[color]
        path = []
        while node not in path:
            for neighbor in node.neighbors:
                if neighbor is self.start[color]:
                    return True
                if neighbor.value is color and neighbor not in path:
                    path.append(node)
                    node = neighbor
                    break

                elif neighbor is node.neighbors[-1]:
                    for neighbor in node.neighbors:
                        if neighbor.value is '_':
                            return True
                    if self.debug:
                        print("Failed due to part complete finish on color: {}".format(color))
                    return False
        if self.debug:
            print("Failed due to part complete finish on color: {}".format(color))
        return False
