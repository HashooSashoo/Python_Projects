import matplotlib

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
