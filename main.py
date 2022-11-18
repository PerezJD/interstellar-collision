import time
from datetime import date

from Space import Space
from Vector3 import Vector3
from InterstellarObject import InterstellarObject

# Notes:
#
# https://solarsystem.nasa.gov/missions/dawn/mission/faq/
# Asteroids are not distributed uniformly in the asteroid belt, but could be approximated to be evenly spaced
# in a region from 2.2 AU (1 AU is 93 million miles, or the average distance between Earth and the Sun) to 3.2 AU
# from the Sun and extending 0.5 AU above and below the ecliptic (the plane of Earth's orbit, which is a convenient
# reference for the solar system). That yields a volume of roughly 16 cubic AU, or about 13 trillion trillion cubic
# miles. (Note: space is big!)
#
# https://solarsystem.nasa.gov/:
# The belt is estimated to contain between 1.1 and 1.9 million asteroids larger than 1 kilometer (0.6 miles) in diameter
# and millions of smaller ones.
#
# Asteroid belt is about 1AU by .5AU
#
# So to roughly simulate the asteroid belt:
#   - 2 million objects with diameter between 1m 1km
#   - 2 million objects with diameter between 1km and 530km. Largest asteroid is ~530 kilometers in diameter
#
# Then divide both by 16 (cubic AU volume of asteroid belt) and combine to get a group of objects to distribute
# through 1 cubic AU of space
#
# https://science.org
# 10% lightspeed would get a craft to Alpha Centauri in 44 years.
# thus 5% lightspeed (our target speed) would take twice as long, or 88 years
#
# https://imagine.gsfc.nasa.gov/features/cosmic/nearest_star_info.html
# Proxima Centauri, the closest star to our own, is still 40,208,000,000,000 km away. (Or about 268,770 AU.)
# 4.246 lightyears
#

# Constants
DAYS_IN_YEAR = 365
METER = .001  # 1 meter base unit. Scaled down for efficiency
KILOMETER = 1000 * METER
AU = 149597870700 * METER  # astronomical unit. Space is very big. from https://cneos.jpl.nasa.gov/glossary/au.html
SPEED_OF_LIGHT_PER_DAY = 173 * AU  # speed of light is 173 astronomical units a day
LIGHTYEAR = 63241.1 * AU  # Distance light travels in one year
ORIGIN = Vector3(0, 0, 0)  # The center of the universe

# "Large" and "small" iso sizes are based on data from https://solarsystem.nasa.gov/ cited above

# Objects with diameter between between 1m and 1km
SMALL_ISO_MIN_RADIUS = METER / 2
SMALL_ISO_MAX_RADIUS = KILOMETER / 2

# Objects with diameter between 1km and 530km.
LARGE_ISO_MIN_RADIUS = KILOMETER / 2
LARGE_ISO_MAX_RADIUS = (530 * KILOMETER) / 2

ISO_MAX_SPEED = 1546560  # Avg. max speed of an iso in 1 day. Based on 17.9km/s from quora, so might not be accurate


def begin_voyage(
    ship_name,
    ship_radius,
    ship_travel_distance,
    ship_speed,
    sector_size,
    large_isos,
    small_isos
):
    # Get the current stardate
    today = date.today()
    stardate = f'{(today.year - 1900)}{today.strftime("%m")}.{today.day}'

    print(f'\nCaptain\'s Log. Stardate: {stardate}. These are the voyages of the starship {ship_name}.')

    # For fun, track how long the simulation takes to run
    start_time = time.time()

    # Perform measurement conversions
    actual_ship_radius = ship_radius * METER
    actual_ship_travel_distance = ship_travel_distance * LIGHTYEAR
    actual_ship_speed = ship_speed * SPEED_OF_LIGHT_PER_DAY
    actual_sector_size = sector_size * LIGHTYEAR

    # Convert size to axis limit.
    # Ex. If sector is 1 cubic lightyear the limit of each axis is .5 lightyears from the origin
    sector_size_limit = actual_sector_size / 2

    # Create the starship
    starship = InterstellarObject(
        actual_ship_radius,
        ORIGIN,
        Vector3.velocity_vector(actual_ship_speed, Vector3.new_random_vector(0, sector_size_limit))
    )

    # Create a sector of space to fly through and populate it with interstellar objects
    sector = Space(sector_size_limit)
    sector.create_interstellar_objects(small_isos, SMALL_ISO_MIN_RADIUS, SMALL_ISO_MAX_RADIUS, ISO_MAX_SPEED, starship)
    sector.create_interstellar_objects(large_isos, LARGE_ISO_MIN_RADIUS, LARGE_ISO_MAX_RADIUS, ISO_MAX_SPEED, starship)

    print(f'\nCourse laid in, Captain. Launching {ship_name} from origin with velocity: {starship.velocity.coordinate}')
    print(f'\nEngage!')

    distance_traveled = 0
    days_travelled = 0

    # Engage!
    while distance_traveled < actual_ship_travel_distance:
        days_travelled += 1

        # First update the ship's position
        starship.update_position(days_travelled)
        distance_traveled = Vector3.distance_between_vectors(ORIGIN, starship.position)

        # Captains Log
        print(f'\nDay: {days_travelled}. Ship position: {starship.coordinate}. Distance Travelled: {distance_traveled}')

        # Now update all the ios's and calculate collisions
        for iso in sector.isos:
            iso.update_position(days_travelled)

            if InterstellarObject.collision(starship, iso):
                # There was a collision. Log it and exit the program
                print(f'\nCollision at {starship.coordinate}')
                exit()

    execution_time = (time.time() - start_time)
    print('\nExecution time in minutes: ' + str(execution_time / 60))


if __name__ == '__main__':

    # Voyage configuration options.
    ship_name = "Enterprise"
    ship_radius = 162.7827 * METER  # Avg. of dimensions of a Federation Constitution class starship from Wikipedia
    ship_travel_distance = 1  # Distance the ship will travel in light years
    ship_speed = .05  # Percentage of light speed the ship will travel at
    sector_size = 2  # Size of our sector in cubic lightyears
    large_isos = 10000  # Number of large interstellar bodies to (potentially) encounter
    small_isos = 10000  # Number of small interstellar bodies to (potentially) encounter

    begin_voyage(ship_name, ship_radius, ship_travel_distance, ship_speed, sector_size, large_isos, small_isos)
