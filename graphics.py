import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

'''
CREATE PLOTTING ENVIRONMENT
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
plt.show()

CHANGE COLOR OF PLOTTING ENVIRONMENT
ax.set_facecolor('blue')      # hex code works too

PLOT LINE THROUGH TWO POINTS
ax.plot([x1, x2], [y1, y2])

CHANGE COLOR OF LINE
ax.plot([x1, x2], [y1, y2], color='green')  # or 'c=' works too
# or after creation:
line.set_color('green')

PLOT RECTANGLE AT A POINT
from matplotlib.patches import Rectangle
rect = Rectangle((x, y), width, height)  # (x, y) is bottom-left corner
ax.add_patch(rect)

CHANGE COLOR OF RECTANGLE
rect = Rectangle((x, y), width, height, facecolor='red', edgecolor='black')
# or after creation:
rect.set_facecolor('red')
rect.set_edgecolor('black')
'''

'''
given a point in 3D space, the projection of that point on the screen is
(x', y') = (x/z, y/z)
'''

'''
-0.5 -> 0.5    0 -> 1
'''
# takes cartesian (x, y) and turns it into values plt can accurately show
def cartesian_to_plt(x, y):
    # shift up 0.5, then shift down by half its width and shift left by half its length
    return (x+0.5, y+0.5)

fig, ax = plt.subplots()
ax.set_aspect('equal')

def plot_rectangle_at_point(x, y, width, height):  
    pyt_points = cartesian_to_plt(x, y)
    shifted_pyt_points = (pyt_points[0] - width/2, pyt_points[1] - height/2)
    rect = Rectangle(shifted_pyt_points, width, height)
    ax.add_patch(rect)
    return rect

plt.show()
