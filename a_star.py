class Node():
    def __init__(self, pos = None, parent = None):
        self.pos = pos
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0
    
    def __eq__(self, other):
        return self.pos == other.pos
    
    def manhattan_dist(self, other):
        return abs(self.pos[0] - other.pos[0]) + \
        abs(self.pos[1] - other.pos[1])

def astar(start_pos, end_pos, map):
    start = Node(start_pos)
    end = Node(end_pos)

    open_list = [start]
    closed_list = []

    while len(open_list) > 0:
        q = open_list[0]
        q_i = 0
        # print(curr.pos)

        for i, n in enumerate(open_list):
            if n.f < q.f:
                q = n
                q_i = i

        open_list.pop(q_i)

        # goal acheived
        if q == end:
            print("goal achieved!")
            path = []
            c = q
            while c is not None:
                path.append(c.pos)
                c = c.parent
            return path[::-1]
        
        # generate children
        children = []

        # change -1 for different step size
        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), \
                        (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            node_pos = (q.pos[0] + new_pos[0], q.pos[1] + new_pos[1])

            if any([node_pos[0] > len(map) - 1, \
                    node_pos[1] > len(map[len(map) - 1]) - 1, \
                    node_pos[0] < 0, node_pos[1] < 0]):
                continue

            if map[node_pos[0]][node_pos[1]] != 0:
                continue

            new_child = Node(node_pos, q)
            children.append(new_child)
        
        for child in children:
            for n in closed_list:
                if child == n and n.f < child.f:
                    continue
            
            child.g = q.g + 1
            # child.h = child.manhattan_dist(end)
            # child.h = abs(child.pos[0] - end.pos[0]) + \
            #     abs(child.pos[1] - end.pos[1])
            child.h = ((child.pos[0] - end.pos[0]) ** 2) + ((child.pos[1] - end.pos[1]) ** 2)
            child.f = child.g + child.h

            for n in open_list:
                if child == n and n.f < child.f:
                    continue
            
            open_list.append(child)

        closed_list.append(q)


def main():

    maze = [[0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    
    

    start = (0, 0)
    end = (3, 2)

    path = astar(start, end, maze)
    print(path)

    x_list = [p[0] for p in path]
    y_list = [p[1] for p in path]

    print(x_list)
    print(y_list)


if __name__ == '__main__':
    main()