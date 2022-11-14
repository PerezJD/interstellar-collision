from Vector3 import Vector3


class InterstellarObject:

    def __init__(self, radius, position, velocity):
        self.radius = radius  # To keep the collision math as simple as possible, we will model everything as a sphere
        self.originalPosition = position  # starting position
        self.position = position  # current calculated position
        self.velocity = velocity

    @property
    def coordinate(self):
        return self.position.coordinate

    def update_position(self, time):
        self.position = InterstellarObject.calculate_new_position(
            self.originalPosition,
            self.velocity,
            time
        )

    @staticmethod
    def calculate_new_position(original_position, velocity, time):
        return Vector3.add_vectors(original_position, Vector3.multiply_by_scalar(velocity, time))

    @staticmethod
    def collision(iso1, iso2):
        distance_between = Vector3.distance_between_vectors(iso1.position, iso2.position)
        return distance_between < (iso1.radius + iso2.radius)
