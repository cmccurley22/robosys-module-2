import matplotlib.pyplot as plt
import pandas as pd

from a_star import Node, astar

data = pd.read_csv("pathflight.csv")

x = data["x"].tolist()
y = data["y"].tolist()

maze = 6 * [[0] * 8]  

start = (0, 0)
end = (3, 2)

path = astar(start, end, maze)
print(path)

x_list = [p[0] * .3 for p in path]
y_list = [p[1] * .3 for p in path]


plt.plot(x, y)
plt.plot(x_list, y_list)
plt.title("Planned and Measured 2D Flight Path")
plt.xlabel("x position (m)")
plt.ylabel("y position (m)")
plt.legend("Measured Path", "Planned Path")

plt.show()
