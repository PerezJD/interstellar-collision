from random import uniform

from InterstellarObject import InterstellarObject
from Vector3 import Vector3


class Space:

    def __init__(self, size_limit):
        # Size of space in cubic astronomical units.
        # We will use this as our range limit when generating positional vectors
        self._size_limit = size_limit

        # List of tracked interstellar objects in this area of space
        self.isos = []

    def create_interstellar_objects(self, num_objects, min_radius, max_radius, max_speed, avoid=None):
        for x in range(num_objects):
            self.isos.append(self.create_iso(min_radius, max_radius, max_speed, avoid))

    def create_iso(self, min_radius, max_radius, max_speed, avoid=None):
        random_radius = uniform(min_radius, max_radius)  # A random size between the designated radius limits
        random_position = Vector3.new_random_vector(0, self._size_limit)   # random position within our area of space
        random_speed = uniform(0, max_speed)  # minimum speed is 0
        random_velocity = Vector3.velocity_vector(random_speed, Vector3.new_random_vector(0, self._size_limit))

        iso = InterstellarObject(
            random_radius,
            random_position,
            random_velocity
        )

        # TODO: Make sure this new iso isn't colliding with any existing isos

        # Make sure we aren't colliding with the avoid object if one was passed
        if avoid is not None and InterstellarObject.collision(iso, avoid):
            print('Invalid starting position for interstellar object. Re-generating')
            return self.create_iso(min_radius, max_radius, max_speed, avoid)

        return iso
