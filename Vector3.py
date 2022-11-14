import math
from random import uniform


class Vector3:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def coordinate(self):
        return f'({self.x}, {self.y}, {self.z})'

    @property
    def magnitude(self):
        xsq = math.pow(self.x, 2)
        ysq = math.pow(self.y, 2)
        zsq = math.pow(self.z, 2)
        return math.sqrt(xsq + ysq + zsq)

    def equals(self, v):
        return self.x == v.x and self.y == v.y and self.z == v.z

    @staticmethod
    def new_random_vector(minimum, maximum):
        return Vector3(
            uniform(minimum, maximum),
            uniform(minimum, maximum),
            uniform(minimum, maximum)
        )

    @staticmethod
    def add_vectors(v1, v2):
        return Vector3(
            v1.x + v2.x,
            v1.y + v2.y,
            v1.y + v2.y
        )

    @staticmethod
    def multiply_by_scalar(v, s):
        return Vector3(
            v.x * s,
            v.y * s,
            v.z * s
        )

    @staticmethod
    def distance_between_vectors(v1, v2):
        x_dif = math.pow(v2.x - v1.x, 2)
        y_dif = math.pow(v2.y - v1.y, 2)
        z_dif = math.pow(v2.z - v1.z, 2)
        return math.sqrt(x_dif + y_dif + z_dif)

    @staticmethod
    def normalize(v):
        magnitude = v.magnitude
        return Vector3(
            v.x/magnitude,
            v.y/magnitude,
            v.z/magnitude
        )

    @staticmethod
    def velocity_vector(speed, direction=None):
        scalar = speed / direction.magnitude
        return Vector3.multiply_by_scalar(direction, scalar)