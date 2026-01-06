import math
import time
from typing import Tuple
import keyboard


def clear_terminal() -> None:
    # Use ANSI escape codes: clear screen and move cursor to top-left
    print('\033[2J\033[1;1H', end='', flush=True)

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

remove_duplicates = lambda x : list(dict.fromkeys(x))

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    #---------------------------POINT BASIC OPERATIONS-------------------------------------------
    def __add__(self, other_point):
        return Point3D(self.x + other_point.x, self.y + other_point.y, self.z + other_point.z)
    
    def __iadd__(self, other_point):
        self.x += other_point.x
        self.y += other_point.y
        self.z += other_point.z
    
    def add(self, other_point):
        self.x += other_point.x
        self.y += other_point.y
        self.z += other_point.z

    def __sub__(self, other_point):
        return Point3D(self.x - other_point.x, self.y - other_point.y, self.z - other_point.z)
    
    def __isub__(self, other_point):
        self.x -= other_point.x
        self.y -= other_point.y
        self.z -= other_point.z
    
    def sub(self, other_point):
        self.x -= other_point.x
        self.y -= other_point.y
        self.z -= other_point.z

    def __matmul__(self, other_point): # Dot product
        return (self.x * other_point.x) + (self.y * other_point.y) + (self.z * other_point.z)
    
    def dot(self, other_point):
        return (self.x * other_point.x) + (self.y * other_point.y) + (self.z * other_point.z)

    def __mul__(self, other_point): # Cross product
        return Point3D((self.y * other_point.z) - (self.z * other_point.y),
                       (self.z * other_point.x) - (self.x * other_point.z),
                       (self.x * other_point.y) - (self.y * other_point.x))
    
    def cross(self, other_point):
        return Point3D((self.y * other_point.z) - (self.z * other_point.y),
                       (self.z * other_point.x) - (self.x * other_point.z),
                       (self.x * other_point.y) - (self.y * other_point.x))

    def translate(self, x_t: float, y_t: float, z_t: float):
        self.x = self.x + x_t
        self.y = self.y + y_t
        self.z = self.z + z_t
        
    # rotation along the Z axis
    def rotateXY(self, theta: float):
        old_x = self.x
        old_y = self.y
        self.x = old_x * math.cos(theta) - old_y * math.sin(theta)
        self.y = old_x * math.sin(theta) + old_y * math.cos(theta)
        self.z = self.z
    
    # rotation along the X axis
    def rotateYZ(self, phi: float):
        old_y = self.y
        old_z = self.z
        self.x = self.x
        self.y = old_y * math.cos(phi) - old_z * math.sin(phi)
        self.z = old_y * math.sin(phi) + old_z * math.cos(phi)
    
    # rotation along the Y axis
    def rotateXZ(self, rho: float):
        old_x = self.x
        old_z = self.z
        self.x = old_x * math.cos(rho) - old_z * math.sin(rho)
        self.y = self.y
        self.z = old_x * math.sin(rho) + old_z * math.cos(rho)

    def rotateOnAllAxes(self, theta: float):
        old_x = self.x
        old_y = self.y
        self.x = old_x * math.cos(theta) - old_y * math.sin(theta)
        self.y = old_x * math.sin(theta) + old_y * math.cos(theta)

        old_y = self.y
        old_z = self.z
        self.y = old_y * math.cos(theta) - old_z * math.sin(theta)
        self.z = old_y * math.sin(theta) + old_z * math.cos(theta)

        old_x = self.x
        old_z = self.z
        self.x = old_x * math.cos(theta) - old_z * math.sin(theta)
        self.z = old_x * math.sin(theta) + old_z * math.cos(theta)

    def rotateSpecified(self, theta, phi, rho):
        self.rotateXY(theta)
        self.rotateYZ(phi)
        self.rotateXZ(rho)

class Line3D:
    def __init__(self, point1: Point3D, point2: Point3D):
        t = 0.05 # parameterize a lot of points that will be our line (i guess determines the resolution??)
        self.point1 = point1
        self.point2 = point2

        t_incX = (self.point2.x - self.point1.x) * t
        t_incY = (self.point2.y - self.point1.y) * t
        t_incZ = (self.point2.z - self.point1.z) * t

        self.pointList = []
        for i in range(int(1/t) + 1):
            self.pointList.append(Point3D(self.point1.x + t_incX*i, self.point1.y + t_incY*i,
                                          self.point1.z + t_incZ*i))
            
        # Wanna add methods to shrink, elongate, change, do a lot of stuff to a line
            
class Object3D:
    def __init__(self, vertex_list: list[Point3D], mapping_list: dict):
        self.vertex_list = vertex_list
        self.mapping_list = mapping_list

        # The dictionary will contain a number of the index of that point, and then the
        # list of all the other indexes that it maps to, so that it can draw line to them
        # (it cannot map to itself)

    def translate(self, x, y, z):
        for vertex in self.vertex_list:
            vertex.translate(x, y, z)

    def rotate_amount(self, theta, phi, rho):
        for vertex in self.vertex_list:
            vertex.translate(-self.origin.x, -self.origin.y, -self.origin.z)
            vertex.rotateSpecified(theta, phi, rho)
            vertex.translate(self.origin.x, self.origin.y, self.origin.z)
    
    def rotate_around_axis(self, theta, phi, rho):
        for vertex in self.vertex_list:
            vertex.rotateSpecified(theta, phi, rho)








    


            

class Cube():
    def __init__(self, origin: Point3D = Point3D(0,0,2), sideLength: float = 3, 
                 xRot: float = 0, yRot: float = 0, zRot: float = 0):
        self.origin = origin
        self.sideLength = sideLength

        # Note the notation for the positions of the cube vertices (original placements)
        # L = left, R - right (x axis)
        # U = up, D = down (y axis)
        # F = front, B = back (z axis)

        self.vertexRUF = Point3D(origin.x + sideLength / 2, origin.y + sideLength / 2, origin.z + sideLength / 2)
        self.vertexRUB = Point3D(origin.x + sideLength / 2, origin.y + sideLength / 2, origin.z - sideLength / 2)
        self.vertexRDF = Point3D(origin.x + sideLength / 2, origin.y - sideLength / 2, origin.z + sideLength / 2)
        self.vertexRDB = Point3D(origin.x + sideLength / 2, origin.y - sideLength / 2, origin.z - sideLength / 2)
        self.vertexLUF = Point3D(origin.x - sideLength / 2, origin.y + sideLength / 2, origin.z + sideLength / 2)
        self.vertexLUB = Point3D(origin.x - sideLength / 2, origin.y + sideLength / 2, origin.z - sideLength / 2)
        self.vertexLDF = Point3D(origin.x - sideLength / 2, origin.y - sideLength / 2, origin.z + sideLength / 2)
        self.vertexLDB = Point3D(origin.x - sideLength / 2, origin.y - sideLength / 2, origin.z - sideLength / 2)

        self.vertexList = [self.vertexRUF, self.vertexRUB, self.vertexRDF, self.vertexRDB, self.vertexLUF, self.vertexLUB, self.vertexLDF, self.vertexLDB]

        # The following is a bunch of manual connections for the lines in the cube :(
        self.frontLine1 = Line3D(self.vertexRUF, self.vertexRDF)
        self.frontLine2 = Line3D(self.vertexRUF, self.vertexLUF)
        self.frontLine3 = Line3D(self.vertexRDF, self.vertexLDF)
        self.frontLine4 = Line3D(self.vertexLUF, self.vertexLDF)

        self.backLine1 = Line3D(self.vertexRUB, self.vertexRDB)
        self.backLine2 = Line3D(self.vertexRUB, self.vertexLUB)
        self.backLine3 = Line3D(self.vertexRDB, self.vertexLDB)
        self.backLine4 = Line3D(self.vertexLUB, self.vertexLDB)

        self.sideLine1 = Line3D(self.vertexRUF, self.vertexRUB)
        self.sideLine2 = Line3D(self.vertexRDF, self.vertexRDB)
        self.sideLine3 = Line3D(self.vertexLDF, self.vertexLDB)
        self.sideLine4 = Line3D(self.vertexLUF, self.vertexLUB)

        self.lineList = [self.frontLine1, self.frontLine2, self.frontLine3, self.frontLine4,
                         self.backLine1, self.backLine2, self.backLine3, self.backLine4,
                         self.sideLine1, self.sideLine2, self.sideLine3, self.sideLine4]

    def reconstruct_lines(self):
        self.frontLine1 = Line3D(self.vertexRUF, self.vertexRDF)
        self.frontLine2 = Line3D(self.vertexRUF, self.vertexLUF)
        self.frontLine3 = Line3D(self.vertexRDF, self.vertexLDF)
        self.frontLine4 = Line3D(self.vertexLUF, self.vertexLDF)

        self.backLine1 = Line3D(self.vertexRUB, self.vertexRDB)
        self.backLine2 = Line3D(self.vertexRUB, self.vertexLUB)
        self.backLine3 = Line3D(self.vertexRDB, self.vertexLDB)
        self.backLine4 = Line3D(self.vertexLUB, self.vertexLDB)

        self.sideLine1 = Line3D(self.vertexRUF, self.vertexRUB)
        self.sideLine2 = Line3D(self.vertexRDF, self.vertexRDB)
        self.sideLine3 = Line3D(self.vertexLDF, self.vertexLDB)
        self.sideLine4 = Line3D(self.vertexLUF, self.vertexLUB)

        # IMPORTANT: Update lineList with the new line objects!
        self.lineList = [self.frontLine1, self.frontLine2, self.frontLine3, self.frontLine4,
                         self.backLine1, self.backLine2, self.backLine3, self.backLine4,
                         self.sideLine1, self.sideLine2, self.sideLine3, self.sideLine4]
    
    def rotate_amount(self, theta, phi, rho):
        for vertex in self.vertexList:
            vertex.translate(-self.origin.x, -self.origin.y, -self.origin.z)
            vertex.rotateSpecified(theta, phi, rho)
            vertex.translate(self.origin.x, self.origin.y, self.origin.z)
        self.reconstruct_lines()

    def translate(self, x, y, z):
        self.origin.translate(x, y, z)
        for vertex in self.vertexList:
            vertex.translate(x, y, z)
        self.reconstruct_lines()

    def outputDisplayMap(self):
        pointList = []
        for line in self.lineList:
            pointList = pointList + line.pointList
        return remove_duplicates(pointList)


# i know kinda jank that point2d isnt defined as a class but whatever lol
# adding a scaling (FOV) factor
def three_dim_to_two_dim(point3D, fov=60):
    fov_rad = math.radians(fov)
    scale = 1 / math.tan(fov_rad / 2)

    newX = (point3D.x / (point3D.z + 1)) * scale
    newY = (point3D.y / (point3D.z + 1)) * scale
    return (newX, newY)

X_DIM = 100
Y_DIM = 50
CLEAR_MAP = [[" " for _ in range(X_DIM)] for _ in range(Y_DIM)]
FULL_MAP = [["@" for _ in range(X_DIM)] for _ in range(Y_DIM)]

class Map:
    def __init__(self, dimensions: Tuple[int, int] = (X_DIM, Y_DIM), content: list[list[str]] = CLEAR_MAP):
        if not isinstance(dimensions, Tuple):
            raise TypeError("Dimensions must be a tuple value with two integers at least 10 or higher.")
        elif len(dimensions) != 2:
            raise ValueError("Dimensions must be a tuple value with two integers at least 10 or higher.")
        elif (dimensions[0] < 10) | (dimensions[1] < 10):
            raise ValueError("Dimensions must be a tuple value with two integers at least 10 or higher.")
        else:
            self.dimensions = dimensions
        
        if not isinstance(content, list):
            raise TypeError("Must add string with amount of characters as your dimensions multiplied together.")
        else:
            self.content = content

        
    def pointValue(self, coord: Tuple[int, int]):
        return self.content[coord[0]][coord[1]]
    
    def clearMap(self):
        self.content = [[" " for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]

    # We will assume that we will be using all of our coordinates in a [-2,2] <- X, [-2,2] <- Y range
    def cartesian_to_poxels(self, coords: Tuple[float, float]) -> Tuple[int, int]:
        # Remember, [-2,2] -> {0,1,...,dimX-1} (for X), [-2,2] -> {0,1,...,dimY-1} (for Y)
        scaledAndRoundedX = round((coords[0] + 2) * (self.dimensions[0] / 4)) # -> {0,1,...dimX-1}
        # Flip Y axis: higher Y values should be at top (lower row indices)
        scaledAndRoundedY = round((2 - coords[1]) * (self.dimensions[1] / 4)) # -> {0,1,...,dimY-1}
        return (scaledAndRoundedY, scaledAndRoundedX)  # Return (row, col)
    
    # Explanation of parameters
    #   listOfCoords: list of tuples that contain of the coords we are writing/deleting
    #   clearMap: list of boolean values the same size of listOfCoords. This tells up which of these coords involve
    #             us writing (bool = False), and which involve us deleting (bool = True)
    def draw_points(self, listOfCoords: list[Tuple[float, float]]):
        self.clearMap()
        listOfCoords = remove_duplicates(listOfCoords)
        for coord in listOfCoords:
            # Bounds checking to prevent index errors
            if 0 <= coord[0] < self.dimensions[1] and 0 <= coord[1] < self.dimensions[0]:
                self.content[coord[0]][coord[1]] = "@"

    
    def displayMap(self):
        print("-" * self.dimensions[0])
        output = []
        for content_list in self.content:
            output.append(''.join(content_list))
        print('\n |'.join(output), end='', flush=True)

    # Combination of all the methods above, takes in an array of 3D points and outputs a 2D output.
    def pointsToImage(self, points_list: list[Point3D]):
        points_2d = [three_dim_to_two_dim(point) for point in points_list if point.z >= 0]
        filtered_points = [point for point in points_2d if ((abs(point[0]) <= 2) and (abs(point[1]) <= 2))]
        poxelated_points = [self.cartesian_to_poxels(point) for point in filtered_points]
        self.draw_points(poxelated_points)
        self.displayMap()

# Now let's configure the terminal as a place to store our games.

display_map = Map()
cube = Cube(Point3D(-4,0,6)) # last three are rotation arguments, will make default = 0 soon.
cube2 = Cube(Point3D(4,0,6))


def animationLoop(t):
    clear_terminal()
    cube.rotate_amount(0.03, 0.05, 0.02)
    cube2.rotate_amount(0.01, 0.05, 0.07)
    cube_points = cube.outputDisplayMap()
    cube2_points = cube2.outputDisplayMap()
    final_points = remove_duplicates(cube_points + cube2_points)
    display_map.pointsToImage(final_points)


t = 0.001
while True:
    animationLoop(t)
    time.sleep(0.01)


