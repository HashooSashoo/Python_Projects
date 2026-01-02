import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

'''
SCRAP IT, we will use the terminal instead
'''

'''
given a point in 3D space, the projection of that point on the screen is
(x', y') = (x/z, y/z)
'''

'''
Order of points
@@@@@@ - 1
###### - 2
====== - 3
|||||| - 4
...... - 5
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

    def rotateOnAllAxes(self, theta):
        self.x = self.x * math.cos(theta) - self.y * math.sin(theta)
        self.y = self.x * math.sin(theta) + self.y * math.cos(theta)

        self.y = self.y * math.cos(theta) - self.z * math.sin(theta)
        self.z = self.y * math.sin(theta) + self.z * math.cos(theta)

        self.x = self.x * math.cos(theta) - self.z * math.sin(theta)
        self.z = self.z * math.sin(theta) + self.z * math.cos(theta)


class Cube():
    def __init__(self, origin: Point3D, sideLength: float, 
                 xRot: float, yRot: float, zRot: float):
        self.origin = origin
        self.sideLength = sideLength

        self.vertex1 = Point3D(origin.x + sideLength / 2, origin.x + sideLength / 2, origin.z + sideLength / 2)
        

        

        


# 3D points we will define
vertex1 = Point3D(-0.25, 0.25, 1.25)
vertex2 = Point3D(0.25, 0.25, 1.25)
vertex3 = Point3D(0.25, -0.25, 1.25)
vertex4 = Point3D(-0.25, -0.25, 1.25)
vertex5 = Point3D(-0.25, 0.25, 1.5)
vertex6 = Point3D(0.25, 0.25, 1.5)
vertex7 = Point3D(0.25, -0.25, 1.5)
vertex8 = Point3D(-0.25, -0.25, 1.5)

# i know kinda jank that point2d isnt defined as a class but whatever lol
def three_dim_to_two_dim(point3D):
    newX = point3D.x / point3D.z
    newY = point3D.y / point3D.z
    return (newX, newY)

# Now let's configure the terminal as a place to store our games.

for i in range(51):
    if i == 26:
        print(("@" * 50) + ("-") + ("@" * 50))
    print("@" * 101)



plt.show()
