from dataclasses import dataclass
from drone import Directions, Drone
from wind_map import Map
from utils import Directions


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
        """
        move drone from right to left a photo radius until it detects next line is out of border  
        """
        # TODO pass to drone component info about wind
        
        while self.drone.x + self.drone.photo_radius <= self.map.size:
            # move up -> calc distancte to top and move 
            steps = self.drone.calc_dist_to_boundary(Directions.UP)
            self.drone.move_seps(steps, Directions.UP)
            self.drone.move_photo_radius(Directions.RIGHT)
            steps = self.drone.calc_dist_to_boundary(Directions.DOWN)
            self.drone.move_seps(steps, Directions.DOWN)
            
            if self.drone.x + self.drone.photo_radius >= self.map.size:
                break
            else:
                self.drone.move_photo_radius(Directions.RIGHT)

        self.map.upload_drone_movent(self.drone.points)
        self.map.show_map(True)



@dataclass()
class Vertical(Route):
    pass


@dataclass()
class Hilbert(Route):
    pass
