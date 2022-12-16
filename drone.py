from dataclasses import dataclass, field
from utils import Directions

class BatteryException(Exception):
    #TODO: stats dump to pdf
    pass

@dataclass()
class Drone:
    # TODO: rewrite Directions from 
    battery: float
    battery_usage: float
    photo_radius: int
    overlap: float
    move_method: str
    wind_direction: str
    map_size: int
    wind_start: int
    wind_stop: int
    x: int = field(init=False)
    y: int = field(init=False)
    __iner_task__: dict = field(init=False)

    def __post_init__(self):
        self.__iner_task__ = {"staus": "none"}
        match self.move_method:
            case "v":
                self.x = int(self.photo_radius)+1
                self.y = 0
            case "h":
                self.x = 0
                self.y = int(self.photo_radius)+1


    def __str__(self) -> str:
        print(self.__iner_task__)
        text = f"Position ({self.x},{self.y})\n Battery: ({self.battery})"
        return text

    def drain_battery(self, factor) -> None:
        """
        Handler for battery drain, raises BatteryException when empty
        """
        self.battery -= (self.battery_usage * factor).__round__(2)
        if self.battery <= 0:
            raise BatteryException
    
    def get_wind_val(self) -> int:
        """
        Return value of wind on drone coords
        """
        return 0

    def move(self, direction: Directions) -> None:
        """
        method to move drone one unit in selected direction
        """
        factor = []
        wind_val = self.get_wind_val()
        if wind_val != 0:
            match self.wind_direction:
                case "l":
                    factor = [1.2,1.2,0.8,1.5]
                case "r":
                    factor = [1.2,1.2,1.5,0.8]
        else:
            factor = [1,1,1,1]
        try:
            match direction:
                case Directions.UP:
                    self.drain_battery(factor[0])
                    self.y += 1
                case Directions.DOWN:
                    self.drain_battery(factor[1])
                    self.y -= 1
                case Directions.LEFT:
                    self.drain_battery(factor[2])
                    self.x -= 1
                case Directions.RIGHT:
                    self.drain_battery(factor[3])
                    self.x += 1
                case _:
                    raise ValueError("Direction do not match!")

        except BatteryException:
            print("Battery ends, sadge")

    def move_seps(self, size: int, direction: Directions, take_photo: bool = True) -> bool:
        """
        method to move drone x units on selected direction
        """
        if not self.boundary_detector(size, direction):
            return False

        self.__iner_task__ = {
                "direction": direction,
                "size": size
                }
        for _ in range(size):
            try:
                if take_photo:
                    self.take_photo()
                self.move(direction=direction)
            except BatteryException:
                return False
        return True
    
    def calc_dist_to_boundary(self, direction: Directions) -> int:
        """
        Calculate distance to boudary in selected direction
        """
        match direction:
            case Directions.LEFT:
                distance = self.x
            
            case Directions.RIGHT:
                distance = self.map_size - 1 - self.x

            case Directions.UP:
                distance = self.map_size - 1 - self.y

            case Directions.DOWN:
                distance = self.y

            case _:
                distance = -1

        return distance

    def move_photo_radius(self, direction: Directions):
        """
        move over direction on photo radius units
        """
        self.move_seps(size = self.photo_radius + 1,
                direction = direction,
                take_photo=False
                )
    
    def boundary_detector(self, size, direction) -> bool:
        """
        check if move_seps can be perfomed within boundaries
        """
        if size <= self.calc_dist_to_boundary(direction):
            return True
        else:
            return False

    def take_photo(self):
        """method simulating photo taking"""
        self.drain_battery(0.1)
