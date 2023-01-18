from dataclasses import dataclass, field
from utils import Directions
from wind_map import Map


class BatteryException(Exception):
    # TODO: stats dump to pdf
    def __init__(self, *args: object) -> None:
        super().__init__(*args)



@dataclass()
class Drone:
    # TODO: rewrite Directions from 
    # comment

    battery: float # init value of battery capacity
    battery_usage: float 
    photo_radius: int
    overlap: float
    wind_direction: Directions
    map_size: int
    wind_start: int
    wind_stop: int
    x: int = field(init=False)
    y: int = field(init=False)
    __iner_task__: dict = field(init=False)

    def __post_init__(self):
        self.__iner_task__ = {"staus": "none"}
        self.points = [] #storing drone flight pattern
        self.photo_point = [] #storing photo list
        self.battery_history = [] # storing battery values throught flight to futher plot 
        self.battery_start_value = self.battery 
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        print(self.__iner_task__)
        text = f"Position ({self.x},{self.y})\n Battery: ({self.battery})"
        return text
    
    def __reset_to_start_params__(self):
        """
        Reseting battery, position and photos 
        """
        self.battery = self.battery_start_value
        self.__post_init__()

    def set_starting_poing(self, x, y) -> list:
        """
        method set drone on given coords
        """
        if (0 <= x <= self.map_size) and (0 <= y <= self.map_size):
            return [x, y]
        else:
            raise ValueError(
                f"Drone needs to be placed within the boundary [{0},{self.map_size}], given parameters -> ({x},{y})")

    def drain_battery(self, factor) -> None:
        """
        Handler for battery drain, raises BatteryException when empty
        """
        self.battery -= (self.battery_usage * factor).__round__(2)
        self.battery_history.append(self.battery)
        if self.battery <= 0:
            # raise BatteryException()
            print(f"Battery ends at point ({self.x},{self.y}) after ({len(self.points)}) meters") 

    def get_wind_val(self) -> int:
        """
        Return value of wind on drone coords
        """
        value = self.map.get_wind_val(self.x, self.y)
        return value
    

    def read_map_data(self, map: Map) -> None:
        """
        Method for reading Map class data
        """
        self.map = map
        self.wind_direction = self.map.wind_direction # read new wind direcrtion when inserting new map
        self.__reset_to_start_params__() # reset to starting parameteres when loading new map

    def move(self, direction: Directions) -> None:
        """
        method to move drone one unit in selected direction
        """
        factor = []
        wind_val = self.get_wind_val()

        # take photo before movent

        self.take_photo()

        if wind_val != 0:
            # rewrite to take care about wind value eg: [cosnt * wind_val]
            # print(f"I got wind at position ({self.x},{self.y})")
            match self.wind_direction:
                case Directions.LEFT:
                    factor = [5*(1+wind_val), 5*(1+wind_val), 0.8, 10.0*(1+wind_val)] # IMPORTANT 
                case Directions.RIGHT:
                    factor = [5*(1+wind_val), 5*(1+wind_val), 10.0*(1+wind_val), 0.8] # IMPORTANT
        else:
            factor = [2, 2, 2, 2]
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

        self.points.append([self.x, self.y])

    def move_steps(self, size: int, direction: Directions, take_photo: bool = True) -> bool:
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
        self.move_steps(size=self.photo_radius + 1,
                       direction=direction,
                       take_photo=False
                       )

    def boundary_detector(self, size, direction) -> bool:
        """
        check if move_steps can be perfomed within boundaries
        """
        if size <= self.calc_dist_to_boundary(direction):
            return True
        else:
            return False

    def take_photo(self):
        """
            method simulating photo taking
        """
        # TODO
        photo_points = [
            [x, y] for x in range(self.x - self.photo_radius, self.x + self.photo_radius) for y in
            range(self.y - self.photo_radius, self.y + self.photo_radius)
        ]
        self.photo_point.append(photo_points)
        self.drain_battery(0.1)

    def export_points(self):
        """
        sztuka dla sztuki
        """
        return self.points

    def rth(self) -> None:
        """
        Reurn to starting point (0,0)        
        """
        down_distance = self.calc_dist_to_boundary(Directions.DOWN)
        self.move_steps(down_distance, Directions.DOWN,take_photo=False)
        self.move_steps(self.calc_dist_to_boundary(Directions.LEFT), Directions.LEFT, take_photo=False)



    def plot_battery_usage(self, method: str = "value"):
        """
            Method for plotting battery usage
        """ 
        match method:
            case "percentage":
                data = [(x/self.battery_start_value).__round__(5) for x in self.battery_history]
            case "value":
                data = self.battery_history
            case _:
                raise ValueError

        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax1 = fig.add_subplot(111)
        plt.plot(data)
        print(f"Remain: {data[-1]}% battery")
        plt.show()

        


@dataclass()
class Camera:
    """
        create parameters for camera
    """
    pass


@dataclass()
class BlackBox:
    """ 
        class for storing data about drone position, photo data and  batteryu status 
    """

    map: Map
    drone: Drone

    def __post_init__(self):
        self.data = []

    def save_data(self, pos: list, battery: float, photo: list):
        self.data.append([pos, battery, photo])

    def __str__(self):
        return str(self.data)
