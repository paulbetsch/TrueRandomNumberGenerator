import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math

def get_points_on_circle(radius, center, num_points):
    x0, y0 = center
    points = []
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        y = y0 + (radius * math.sin(theta))
        x = x0 + (radius * math.cos(theta))
        points.append((x, y))
    return points

def draw_circle(radius, center, color):
    circle = Circle(center, radius, fill=False, edgecolor=color)
    ax.add_patch(circle)


radius = 50
fig, ax = plt.subplots()
ax.set_xlim(-200, 200)
ax.set_ylim(-200, 200)

draw_circle(50, (0, 0), 'black') 

points = get_points_on_circle(50, (0,0), 100)
drittesPendel = []

for point in points:
    draw_circle(50, (point[0],point[1]), 'red')
    drittesPendel.append(get_points_on_circle(50, (point[0],point[1]), 100))

for i in drittesPendel:
    for j in i:
        draw_circle(50, (j[0],j[1]), 'green')

plt.show()