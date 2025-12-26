import math
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

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def translate(self, x_t, y_t, z_t):
        self.x = self.x + x_t
        self.y = self.y + y_t
        self.z = self.z + z_t
        
    # rotation along the Z axis
    def rotateXY(self, theta):
        self.x = self.x * math.cos(theta) - self.y * math.sin(theta)
        self.y = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.z = self.z
    
    # rotation along the X axis
    def rotateYZ(self, phi):
        self.x = self.x
        self.y = self.y * math.cos(phi) - self.z * math.sin(phi)
        self.z = self.y * math.sin(phi) + self.z * math.cos(phi)
    
    # rotation along the Y axis
    def rotateXZ(self, rho):
        self.x = self.x * math.cos(rho) - self.z * math.sin(rho)
        self.y = self.y
        self.z = self.z * math.sin(rho) + self.z * math.cos(rho)



# 3D points we will define
vertex1 = Point3D(-0.25, 0.25, 1.25)
vertex2 = Point3D(0.25, 0.25, 1.25)
vertex3 = Point3D(0.25, -0.25, 1.25)
vertex4 = Point3D(-0.25, -0.25, 1.25)
vertex5 = Point3D(-0.25, 0.25, 1.5)
vertex6 = Point3D(0.25, 0.25, 1.5)
vertex7 = Point3D(0.25, -0.25, 1.5)
vertex8 = Point3D(-0.25, -0.25, 1.5)

def three_dim_to_two_dim(point3D):
    newX = point3D[0] / point3D[2]
    newY = point3D[1] / point3D[2]
    return (newX, newY)

# Initialize graphing environment
fig, ax = plt.subplots()
ax.set_aspect('equal')

# The following two functions graph a rectangle at a certain cartesian point 
# (assuming origin is at center and range is -0.5 to 0.5 for both axes)

# takes cartesian (x, y) and turns it into values plt can accurately show
def cartesian_to_plt(x, y):
    # shift up 0.5, then shift down by half its width and shift left by half its length
    return (x+0.5, y+0.5)

def plot_rectangle_at_point(x, y, width, height):  
    pyt_points = cartesian_to_plt(x, y)
    shifted_pyt_points = (pyt_points[0] - width/2, pyt_points[1] - height/2)
    rect = Rectangle(shifted_pyt_points, width, height)
    ax.add_patch(rect)
    return rect

plt.show()
