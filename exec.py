from drone import Directions, Drone
from prep_routes import Horizontal
from wind_map import Distributions, Map

if __name__ == "__main__":
    # create firt working example
    drone = Drone(
        battery=3000,
        battery_usage=1,
        photo_radius=5,
        move_method="v",
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
    # Plan:
    # 1. Generate 100 map
    # 2. Iterate over them witch two drones: one horizontal and one vertical
    # 3. 
