from dataclasses import dataclass
from drone import Drone
from wind_map import Map

@dataclass()
class Route:
    drone: Drone
    map: Map 

    def execute_route(self):
        pass


@dataclass()
class Horizontal(Route):
    drone: Drone
    map: Map

    def execute_route(self):
       pass 


@dataclass()
class Vertical(Route):
    pass


@dataclass()
class Hilbert(Route):
    pass
