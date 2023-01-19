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
    

    @classmethod
    def run_test(cls, drone: Drone, map: Map):
        val = cls(drone, map)
        val.drone.read_map_data(val.map)
        val.execute_route()
        val.stats()

    def stats(self) -> dict:
        return {}


@dataclass()
class Horizontal(Route):
    drone: Drone
    map: Map

    def execute_route(self):
        """
        move drone from right to left a photo radius until it detects next line is out of border  
        """
        # TODO pass to drone component info about wind
        self.drone.read_map_data(self.map)
        while self.drone.x + self.drone.photo_radius <= self.map.size:
            # move up -> calc distancte to top and move 
            steps = self.drone.calc_dist_to_boundary(Directions.UP)
            self.drone.move_steps(steps, Directions.UP)
            self.drone.move_photo_radius(Directions.RIGHT)
            steps = self.drone.calc_dist_to_boundary(Directions.DOWN)
            self.drone.move_steps(steps, Directions.DOWN)
            
            if self.drone.x + self.drone.photo_radius >= self.map.size:
                break
            else:
                self.drone.move_photo_radius(Directions.RIGHT)
        else:
            self.drone.move_steps(self.drone.calc_dist_to_boundary(Directions.UP), Directions.UP)
            self.drone.rth()
        self.map.upload_drone_movent(self.drone.points)
        self.drone.plot_battery_usage(method="percentage")
        self.map.show_map(True)
        


    def stats(self):
        sample = {
                 "completed": True,
                 "photos_captured": len(self.drone.photo_point),
                 "battery_remain": self.drone.battery
                 }

@dataclass()
class Vertical(Route):
    drone: Drone
    map: Map

    def execute_route(self):
        """
        #
        """

        while self.drone.y + self.drone.photo_radius <= self.map.size:
            # move up -> calc distancte to top and move
            steps = self.drone.calc_dist_to_boundary(Directions.RIGHT)
            self.drone.move_steps(steps, Directions.RIGHT)
            self.drone.move_photo_radius(Directions.UP)
            steps = self.drone.calc_dist_to_boundary(Directions.LEFT)
            self.drone.move_steps(steps, Directions.LEFT)

            if self.drone.y + self.drone.photo_radius >= self.map.size:
                break
            else:
                self.drone.move_photo_radius(Directions.UP)

        else:
            self.drone.move_steps(self.drone.calc_dist_to_boundary(Directions.UP), Directions.UP)
            self.drone.rth()
        self.map.upload_drone_movent(self.drone.points)
        self.drone.plot_battery_usage(method="percentage")
        self.map.show_map(True)


@dataclass()
class Hilbert(Route):
    pass
