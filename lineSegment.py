# -*- coding: latin-1 -*-
import numpy as np

def vector_length(vector):
    return (vector[0]**2+vector[1]**2)**0.5

class LineSegment:

    """Represents a line segment on a pixel plane

    Since we are handling pixels there all coordinates are discrete(int)

    Attributes:
        a (Tuple(int,int)): start point nearest to the origin
        b (Tuple(int,int)): end point furthest to the origin
        vector (Tuple(int,int)): the vector itself b-a
        x (int): the vector starting point
        y (int): The vector end point
        unit_vector Tuple(int,int)): the unit vector
        length (int): the size of the vector sqrt(x²+y²)
        angle_precision (int): decimal point precision,defaults to 4
    """

    __slots__ = ['a', 'b', 'x', 'y', 'vector',
                 'unit_vector', 'length', 'angle_precision','dist_to_origin']

    def __init__(self, point_a, point_b, angle_precision=4):
        """
        Args:
            point_a (Tuple(int,int)): Start point
            point_b (Tuple(int,int)): End point
            angle_precision (int): decimal point precision,defaults to 4
        """
        if point_a[0] > point_b[0] or point_a[1] > point_b[1]:
            temp = point_a
            point_a = point_b
            point_b = temp
        self.a = point_a
        self.b = point_b
        self.angle_precision = angle_precision
        self._set_vector()
        self.unit_vector = LineSegment.get_unit_vector(self.x, self.y)

    def _set_vector(self):
        self.vector = [self.b[0]-self.a[0], self.b[1]-self.a[1]]
        self.x = self.vector[0]
        self.y = self.vector[1]
        self.length = vector_length(self.vector)
        self.dist_to_origin = vector_length(self.a)



    @staticmethod
    def get_unit_vector(x, y):
        """Gets the unit vector of a vector

        Args:
            x (int): x coordinate
            y (int): y coordinate
        """
        vector = [x, y]
        length = np.linalg.norm(vector) 
        if(length <= 0.0):
            return None
        norm = vector / length
        return [norm[0], norm[1]]

    def get_angle(self, relative_to=(1, 0)):
        """ get the angle between this segment and some vector
                Args:
                        relative_to (ArrayLike): optional defaults to 1,0
        """
        v2_u = relative_to
        if relative_to != (1, 0):
            v2_u = LineSegment.get_unit_vector(relative_to[0], relative_to[1])
        # Not using the length since we are using both unit vectors
        angle = np.arccos(abs(np.dot(self.unit_vector, v2_u)))
        if np.isnan(angle):
            return 0.0
        return round(angle, self.angle_precision)

    def __repr__(self):
        text = "[(%d,%d),(%d,%d)]  = (%d,%d) %dpx"
        vals = (self.a[0], self.a[1], self.b[0],
                self.b[1], self.x, self.y, self.length)
        return text % vals

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return (self.a[0], self.a[1], self.b[0], self.b[1]).__hash__()
    
    def __lt__(self, other):
        return self.dist_to_origin<other.dist_to_origin

    @staticmethod
    def get_projection(vector, uv):
        """Get the projection of vector on uv
        """
        a1 = np.dot(vector, uv)
        return [a1*uv[0], a1*uv[1]]

    def get_projected_segment(self, to_project):
        projection = LineSegment.get_projection(self.vector, to_project)
        b = [self.a[0]+projection[0], self.a[1]+projection[1]]
        return LineSegment(self.a, b)

    def add_segment(self, segment):
        if segment < self:
            self.a = segment.a
        if vector_length(segment.b) > vector_length(self.b):
            self.b = segment.b
        self._set_vector()
