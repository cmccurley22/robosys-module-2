from room_map import RoomMap

class Node:
    def __init__(self, g, h, parent = None):
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def update(self, g, h, parent):
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __str__(self):
        return f"g: {self.g}, h: {self.h}, f: {self.f}"

class PriorityQueue:
    def __init__(self):
        self.queue = dict()
        self.sorted_queue = []

    def sort(self):
        self.sorted_queue = sorted(self.queue.keys(), key=lambda x: self.queue[x].f)

    def put(self, pos, node):
        self.queue[pos] = node
        self.sort()

    def pop(self):
        current = self.sorted_queue.pop(0)
        del self.queue[current]
        return current
    
def calculate_g(parent_node):
    return parent_node.g + 1

def calculate_h(current_pos, end):
    return abs(current_pos[0] - end[0]) + abs(current_pos[1] - end[1])

def a_star(start, end, room_map = RoomMap()):
    open_q = PriorityQueue()
    closed = set()

    # Add the starting square (or node) to the open list.
    open_q.put(start, Node(0, calculate_h(start, end)))

    while True:
        # Get the lowest F cost square on the open list
        current = open_q.pop()
        # Switch it to the closed list
        closed.add(current)
        # For each of the 8 squares adjacent to current
        for neighbor in room_map.get_neighbors(current):
            # If it is not walkable or if it is on the closed list, ignore it
            if room_map.is_valid_point(neighbor) and neighbor not in closed:
                pass
            # If it isn’t on the open list, make a new node with current as it's parent
            if neighbor not in open_q.queue:
                new_node = Node(calculate_g(current), calculate_h(neighbor, end), current)
                # add it to the open list
                open_q.put(neighbor, new_node)

            # If it is on the open list already, check to see if this path to that square is better, using G cost as the measure
            else:
                new_g = calculate_g(current) + calculate_h(neighbor, end)
                if  new_g < open_q.queue[neighbor].g:
                    # If so, change the parent of the square to the current square, and recalculate the G and F scores of the square
                    open_q.queue[neighbor].update(calculate_g(current), calculate_h(neighbor, end), current)
                    # If you are keeping your open list sorted by F score, you may need to resort the list
                    open_q.sort()

        

if __name__ == "__main__":
    obstacles = [((0, 0.3), (1.22, 0.605), ((0, -0.3), (1.22, -0.605)))]
    room_map = RoomMap(obstacles = obstacles)

    