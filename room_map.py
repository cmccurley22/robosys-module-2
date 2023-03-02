class RoomMap:
    def __init__(self, bot_left = (0.3*-3,0.3*-3), top_right = (0.3*8, 0.3*4), resolution = 0.3, obstacles = []):
        self.bot_left = bot_left
        self.top_right = top_right
        self.resolution = resolution
        self.obstacles = obstacles

    def add_obstacle(self, bot_left, top_right):
        self.obstacles.append((bot_left, top_right))

    def is_valid_point(self, point):
        valid = True
        # Check if out of bounds
        if (
        not self.bot_left[0] <= point[0] <= self.top_right[0] or
        not self.bot_left[1] <= point[1] <= self.top_right[1]
        ):
            valid = False
        # Check if overlapping with an obstacle
        for bot_left, top_right in self.obstacles:
                if (
                not bot_left[0] <= point[0] <= top_right[0] or
                not bot_left[1] <= point[1] <= top_right[1]
                ):
                     valid = False

        return valid
    
    def get_neighbors(self, point):
         """
         Takes a point and returns all valid neighbors
         """
         res = self.resolution
         neighbors = []
         offsets = [
              (0,1), (1,0), (0,-1), (-1,0),
              (1,1), (-1,-1), (-1,1), (1,-1)]

         for offset in offsets:
              current = (point[0] + offset[0] * res, point[1] + offset[1] * res)
              if self.is_valid_point(current):
                   neighbors.append(current)