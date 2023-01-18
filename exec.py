from random import random
from numpy.random import rand
from drone import Directions, Drone
from prep_routes import Horizontal
from wind_map import Distributions, Map

if __name__ == "__main__":
    # create firt working example
    drone = Drone(
        battery=3000,
        battery_usage=1,
        photo_radius=5,
        overlap=10,
        wind_direction=Directions.LEFT,
        map_size=50,
        wind_start=13,
        wind_stop=55
        # wind mod = [3, 1.0, 1.5]
    )

    map = Map(
        size=50,
        wind_size=20,
        photo_radius=3,
        overlap=0.5,
        wind_distribution=Distributions.FIXED_VALUE)
    route = Horizontal(
        drone, map
    )

    route.execute_route()
    
    maps = [] #preparing container for maps

    winds = [Distributions.FIXED_VALUE, Distributions.NORMAL] # make list to select from there 
    winds_stats = { # keep counter of selected wind generators
            Distributions.FIXED_VALUE: 0,
            Distributions.NORMAL: 0
            } 
    
    for _ in range(100): 
        wind = random.choice(winds)
        tmp = Map(
            size=50,
            wind_size=20,
            photo_radius=3,
            overlap=0.5,
            wind_distribution=wind)
        maps.append(tmp)
        winds_stats[wind] += 1


    drone = Drone(
        battery=3000,
        battery_usage=1,
        photo_radius=5,
        overlap=10,
        wind_direction=Directions.LEFT,
        map_size=50,
        wind_start=13,
        wind_stop=55
    )

    drone2 = Drone(
        battery=3000,
        battery_usage=1,
        photo_radius=5,
        overlap=10,
        wind_direction=Directions.LEFT,
        map_size=50,
        wind_start=13,
        wind_stop=55
    )


