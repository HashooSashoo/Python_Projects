import math
import time
from typing import Tuple # only for type hinting, no functionality
from typing import Self # only for type hinting, no functionality
from graphics_helper_funcs import create_triangles # my own script

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

class Point2D:
    def __init__(self, x: float, y: float, write_char="@", z_index=0.0):
        self.x = x
        self.y = y
        self.write_char = write_char
        self.z_index = z_index

# adding this function to add priority for certain characters when removing duplicates in Point2D characters.
# Now uses z-index (depth) as primary sorting criterion, with character priority as tiebreaker
def remove_2d_point_duplicates(point_list: list[Point2D]) -> list[Point2D]:
    PRIORITY_LIST = ['@','#','=','-','.']

    # Group points by their (x, y) coordinates
    # Round coordinates to avoid floating-point precision issues
    coord_dict = {}
    for point in point_list:
        coord_key = (round(point.x, 6), round(point.y, 6))  # Round to 6 decimal places
        if coord_key not in coord_dict:
            coord_dict[coord_key] = []
        coord_dict[coord_key].append(point)

    # For each group, select the point with lowest z_index (closest to camera)
    # If z_index is tied, use character priority as tiebreaker
    result = []
    for coord_points in coord_dict.values():
        if len(coord_points) == 1:
            result.append(coord_points[0])
        else:
            # Find the point with the lowest z_index (closest to camera)
            best_point = coord_points[0]
            best_z = best_point.z_index
            best_char_priority = PRIORITY_LIST.index(best_point.write_char) if best_point.write_char in PRIORITY_LIST else len(PRIORITY_LIST)

            for point in coord_points[1:]:
                point_z = point.z_index
                point_char_priority = PRIORITY_LIST.index(point.write_char) if point.write_char in PRIORITY_LIST else len(PRIORITY_LIST)

                # Lower z_index = closer to camera = higher priority
                # If z_index is very close (within 0.001), use character priority as tiebreaker
                if point_z < best_z - 0.001:  # Significantly closer
                    best_point = point
                    best_z = point_z
                    best_char_priority = point_char_priority
                elif abs(point_z - best_z) <= 0.001:  # Same depth, use character priority
                    if point_char_priority < best_char_priority:
                        best_point = point
                        best_z = point_z
                        best_char_priority = point_char_priority

            result.append(best_point)

    return result


    


class Point3D:
    def __init__(self, x: float, y: float, z: float, write_char="@") -> None:
        self.x = x
        self.y = y
        self.z = z

        self.write_char = write_char

    #---------------------------POINT BASIC OPERATIONS-------------------------------------------
    def __add__(self, other_point: Self) -> Self:
        return Point3D(self.x + other_point.x, self.y + other_point.y, self.z + other_point.z)
    
    def __iadd__(self, other_point: Self) -> None:
        self.x += other_point.x
        self.y += other_point.y
        self.z += other_point.z
    
    def add(self, other_point: Self) -> None:
        self.x += other_point.x
        self.y += other_point.y
        self.z += other_point.z

    def __sub__(self, other_point: Self) -> Self:
        return Point3D(self.x - other_point.x, self.y - other_point.y, self.z - other_point.z)
    
    def __isub__(self, other_point: Self) -> None:
        self.x -= other_point.x
        self.y -= other_point.y
        self.z -= other_point.z
    
    def sub(self, other_point: Self) -> None:
        self.x -= other_point.x
        self.y -= other_point.y
        self.z -= other_point.z

    #-------------------VECTOR OPERATIONS----------------------------------------

    def __abs__(self):
        return math.sqrt((self.x)^2 + (self.y)^2 + (self.z)^2)
    
    def magnitude(self):
        return math.sqrt((self.x)^2 + (self.y)^2 + (self.z)^2)
    
    def __matmul__(self, other_point: Self) -> float: # Dot product
        return (self.x * other_point.x) + (self.y * other_point.y) + (self.z * other_point.z)
    
    def dot(self, other_point: Self) -> float:
        return (self.x * other_point.x) + (self.y * other_point.y) + (self.z * other_point.z)

    def __mul__(self, other_point: Self) -> Self: # Cross product OR scalar multiplication
        if isinstance(other_point, (float, int)):
            return Point3D(self.x * other_point, self.y * other_point, self.z * other_point)
        elif isinstance(other_point, Point3D):
            return Point3D((self.y * other_point.z) - (self.z * other_point.y),
                           (self.z * other_point.x) - (self.x * other_point.z),
                           (self.x * other_point.y) - (self.y * other_point.x))
        else:
            raise ValueError
        
    def __truediv__(self, other_point: Self) -> Self:
        if isinstance(other_point, (float, int)):
            return Point3D(self.x / other_point, self.y / other_point, self.z / other_point)
        else:
            raise ValueError
    
    def cross(self, other_point: Self) -> Self:
        return Point3D((self.y * other_point.z) - (self.z * other_point.y),
                       (self.z * other_point.x) - (self.x * other_point.z),
                       (self.x * other_point.y) - (self.y * other_point.x))

    #-------------------3D SPACE OPERATIONS--------------------------------------------

    def translate(self, x_t: float, y_t: float, z_t: float) -> None:
        self.x = self.x + x_t
        self.y = self.y + y_t
        self.z = self.z + z_t
        
    # rotation along the Z axis
    def rotateXY(self, theta: float) -> None:
        old_x = self.x
        old_y = self.y
        self.x = old_x * math.cos(theta) - old_y * math.sin(theta)
        self.y = old_x * math.sin(theta) + old_y * math.cos(theta)
        self.z = self.z
    
    # rotation along the X axis
    def rotateYZ(self, phi: float) -> None:
        old_y = self.y
        old_z = self.z
        self.x = self.x
        self.y = old_y * math.cos(phi) - old_z * math.sin(phi)
        self.z = old_y * math.sin(phi) + old_z * math.cos(phi)
    
    # rotation along the Y axis
    def rotateXZ(self, rho: float) -> None:
        old_x = self.x
        old_z = self.z
        self.x = old_x * math.cos(rho) - old_z * math.sin(rho)
        self.y = self.y
        self.z = old_x * math.sin(rho) + old_z * math.cos(rho)

    def rotateOnAllAxes(self, theta: float) -> None:
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

    def rotateSpecified(self, theta, phi, rho) -> None:
        self.rotateXY(theta)
        self.rotateYZ(phi)
        self.rotateXZ(rho)

    #-----------------PRINT AND STRING-------------------------------
    def __str__(self) -> str:
        return f"Point Object: ({self.x}, {self.y}, {self.z})"



class Line3D:
    def __init__(self, point1: Point3D, point2: Point3D) -> None:
        self.t = 0.05 # parameterize a lot of points that will be our line (i guess determines the resolution??)
        self.point1 = point1
        self.point2 = point2

        # define the slope of the line (a tuple of three floats)
        self.slope = (self.point2.x - self.point1.x,
                      self.point2.y - self.point1.y,
                      self.point2.z - self.point1.z)

        # creates the increment amount for each component to make the pointlist for the line.
        self.t_inc = tuple(slope_element * self.t for slope_element in self.slope)

        self.pointList = []
        for i in range(int(1/self.t) + 1):
            self.pointList.append(Point3D(self.point1.x + self.t_inc[0]*i, self.point1.y + self.t_inc[1]*i,
                                          self.point1.z + self.t_inc[2]*i, "@"))
            
        # Wanna add methods to shrink, elongate, change, do a lot of stuff to a line

    def change_resolution(self, new_resolution: float):
        if new_resolution >= 0.1:
            print("Warning: Resolution might be too low. Consider values from 0.005 to 0.05.")
        elif new_resolution <= 0.001:
            print("Warning: Resolution might be too high. Consider values from 0.005 to 0.05.")
        self.t = new_resolution

    
    def __str__(self) -> str:
        return f"Line Object: from {self.point1} to {self.point2}"
    

class PlaneTriangle3D:
    def __init__(self, point1: Point3D, point2: Point3D, point3: Point3D):
        # first put all the points in the object
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

        self.pointList = []

        # then actually make the plane (its gonna be a collection of points, or to be more specific, a collection of lines)
        # how we will make the points is we sweep a line from the point1-point2 segment to the point1-point3 segment
        # then we sweep through the angle creating a bunch of new lines from point1 to the points in point2-point3
        boundary_points = Line3D(self.point2, self.point3).pointList
        for boundary_point in boundary_points:
            line_points = Line3D(self.point1, boundary_point).pointList
            self.pointList.extend(line_points)

        # remove any duplicate points to preserve memory
        self.pointList = remove_duplicates(self.pointList)
        for i in range(len(self.pointList)):
            self.pointList[i].write_char = "-"



class Object3D:
    def __init__(self, vertex_list: list[Point3D], mapping_list: tuple[list[int]]) -> None:
        self.vertex_list = vertex_list
        self.mapping_list = mapping_list

        # The dictionary will contain a number of the index of that point, and then the
        # list of all the other indexes that it maps to, so that it can draw line to them
        # (it cannot map to itself)

        self.origin = sum(vertex_list, start=Point3D(0,0,0)) / len(vertex_list)

    def __str__(self) -> str:
        return f"Object3D Object:\nOrigin: {self.origin}\nPoint List: {[str(vertex) for vertex in self.vertex_list]}\nMapping List: {self.mapping_list}"

    def translate(self, x: float, y: float, z: float) -> None:
        self.origin.translate(x, y, z)
        for vertex in self.vertex_list:
            vertex.translate(x, y, z)

    def rotate_amount(self, theta: float, phi: float, rho: float) -> None: # rotation about origin of the object.
        for vertex in self.vertex_list:
            vertex.translate(-self.origin.x, -self.origin.y, -self.origin.z)
            vertex.rotateSpecified(theta, phi, rho)
            vertex.translate(self.origin.x, self.origin.y, self.origin.z)
    
    def rotate_around_axis(self, theta, phi, rho): # rotation about the origin of the coordinate system
        for vertex in self.vertex_list:
            vertex.rotateSpecified(theta, phi, rho)
    
    def generate_line_list(self) -> list[Line3D]:
        line_list = []
        for i in range(len(self.vertex_list)):
            vertex = self.vertex_list[i]
            map_list = self.mapping_list[i]

            for index in map_list:
                line_list.append(Line3D(vertex, self.vertex_list[index]))
        return line_list
    
    def generate_plane_list(self) -> list[PlaneTriangle3D]:
        plane_list = []
        triangle_list = create_triangles(self.mapping_list)

        # Puts all the Point3D objects in an array to use
        for triangle in triangle_list:
            vertices = []
            for vertex in triangle:
                vertices.append(self.vertex_list[vertex])
            
            # append each plane to the plane list
            plane_list.append(PlaneTriangle3D(vertices[0], vertices[1], vertices[2]))
        return plane_list

    def output_display_map(self) -> list[Point3D]:
        point_list = []
        line_list = self.generate_line_list()
        plane_list = self.generate_plane_list()
        for line in line_list:
            point_list = point_list + line.pointList
        for plane in plane_list:
            point_list = point_list + plane.pointList
        return remove_duplicates(point_list)
    

# i know kinda jank that point2d isnt defined as a class but whatever lol
# adding a scaling (FOV) factor
def three_dim_to_two_dim(point3D: Point3D, fov=60) -> Point2D:
    fov_rad = math.radians(fov)
    scale = 1 / math.tan(fov_rad / 2)

    newX = (point3D.x / (point3D.z + 1)) * scale
    newY = (point3D.y / (point3D.z + 1)) * scale
    return Point2D(newX, newY, point3D.write_char, point3D.z)

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
    def cartesian_to_poxels(self, coords: Point2D) -> Point2D:
        # Remember, [-2,2] -> {0,1,...,dimX-1} (for X), [-2,2] -> {0,1,...,dimY-1} (for Y)
        scaledAndRoundedX = round((coords.x + 2) * (self.dimensions[0] / 4)) # -> {0,1,...dimX-1}
        # Flip Y axis: higher Y values should be at top (lower row indices)
        scaledAndRoundedY = round((2 - coords.y) * (self.dimensions[1] / 4)) # -> {0,1,...,dimY-1}
        return Point2D(int(scaledAndRoundedX), int(scaledAndRoundedY), coords.write_char, coords.z_index)  # Return Point2D
    
    # Explanation of parameters
    #   listOfCoords: list of tuples that contain of the coords we are writing/deleting
    #   clearMap: list of boolean values the same size of listOfCoords. This tells up which of these coords involve
    #             us writing (bool = False), and which involve us deleting (bool = True)
    def draw_points(self, listOfCoords: list[Point2D]):
        self.clearMap()
        listOfCoords = remove_2d_point_duplicates(listOfCoords)
        for coord in listOfCoords:
            # Bounds checking to prevent index errors
            if 0 <= coord.x < self.dimensions[0] and 0 <= coord.y < self.dimensions[1]:
                self.content[coord.y][coord.x] = coord.write_char

    
    def displayMap(self):
        print("-" * self.dimensions[0])
        output = []
        for content_list in self.content:
            output.append(''.join(content_list))
        print('\n |'.join(output), end='', flush=True)

    # Combination of all the methods above, takes in an array of 3D points and outputs a 2D output.
    def pointsToImage(self, points_list: list[Point3D]):
        points_2d = [three_dim_to_two_dim(point) for point in points_list if point.z >= 0]
        filtered_points = [point for point in points_2d if (abs(point.x) <= 2) and (abs(point.y) <= 2)]
        poxelated_points = [self.cartesian_to_poxels(point) for point in filtered_points]
        self.draw_points(poxelated_points)
        self.displayMap()

# Now let's configure the terminal as a place to store our games.

display_map = Map()
cube2 = Object3D([Point3D(1,1,1), Point3D(-1,1,1), Point3D(-1,-1,1), Point3D(1,-1,1),
                  Point3D(1,1,3), Point3D(-1,1,3), Point3D(-1,-1,3), Point3D(1,-1,3)],
                  ([1,3,4],[0,2,6],[1,3,6],[0,2,7],[0,5,7],[1,4,6],[2,5,7],[3,4,6]))
cube2.translate(-2,0,2)

triangle_3d = Object3D([Point3D(0,0,1), Point3D(-1,2,3), Point3D(2,1,2)], ([1,2],[0,2],[0,1]))


def animationLoop(t):
    clear_terminal()

    triangle_3d.rotate_amount(0, 0.05, 0.05)
    triangle_points = triangle_3d.output_display_map()

    # cube.rotate_amount(0.03, 0.05, 0.02)
    cube2.rotate_amount(0.03, 0.05, 0.02)
    cube_points = cube2.output_display_map()

    all_points = cube_points + triangle_points
    display_map.pointsToImage(all_points)


t = 0.001
while True:
    animationLoop(t)
    time.sleep(0.01)


