from dataclasses import dataclass
from drone import Drone

@dataclass()
class Route:
    drone: Drone
    
    def execute_route(self):
        pass


@dataclass()
class Horizontal(Route):
    
    def execute_route(self):
        return super().execute_route()


@dataclass()
class Vertical(Route):
    pass


@dataclass()
class Hilbert(Route):
    pass
