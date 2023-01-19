import random
from drone import Directions, Drone
from prep_routes import Horizontal, Vertical
from wind_map import Distributions, Map
import pandas as pd

def callmethod_approach() -> None:
    TEST_SIZE = 100

    drone = Drone(
        battery=4000,
        battery_usage=1,
        photo_radius=5,
        overlap=10,
        wind_direction=Directions.LEFT,
    )
 
    maps = []
    wind_types = [Distributions.FIXED_VALUE, Distributions.NORMAL]

    for x in range(TEST_SIZE):
        wind_type_tmp = random.choice(wind_types)
        x_map = Map(
            size=50,
            wind_size=20,
            photo_radius=3,
            overlap=0.5,
            wind_distribution=wind_type_tmp)
        maps.append(x_map)

    # now, testing time:
    vertical_results = []
    horizontal_results = []
    for map_x in maps:
        v_res = Vertical.run_test(drone, map_x)
        h_res = Horizontal.run_test(drone, map_x)
        vertical_results.append(v_res["battery_remain"])
        horizontal_results.append(h_res["battery_remain"])

    results = list(zip(vertical_results, horizontal_results))
    df = pd.DataFrame(results, columns=["verical", "horizontal"])
    df.to_csv('result.csv', sep=":", decimal=",")
def standard_approcach() -> None:
    pass


if __name__ == "__main__":
    callmethod_approach()


