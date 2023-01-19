from random import random
from numpy.random import rand
from drone import Directions, Drone
from prep_routes import Horizontal
from wind_map import Distributions, Map


def callmethod_approach() -> None:
    drone = Drone(
        battery=3000,
        battery_usage=1,
        photo_radius=5,
        overlap=10,
        wind_direction=Directions.LEFT,
    )

    map = Map(
        size=50,
        wind_size=20,
        photo_radius=3,
        overlap=0.5,
        wind_distribution=Distributions.FIXED_VALUE)
    test = Horizontal.run_test(drone, map)


def standard_approcach() -> None:
    pass


if __name__ == "__main__":
    callmethod_approach()


