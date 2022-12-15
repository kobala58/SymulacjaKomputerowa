from dataclasses import dataclass, field

class BatteryException(Exception):
    #TODO: stats dump to pdf
    pass

@dataclass()
class Drone:
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

    def drain_battery(self, factor):
        self.battery -= (self.battery_usage * factor).__round__(2)
        if self.battery <= 0:
            raise BatteryException
    
    def get_wind_val(self):
        return 0

    def move(self, direction: str):
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
            if direction == "u":
                self.drain_battery(factor[0])
                self.x += 1
            elif direction == "d":
                self.drain_battery(factor[1])
                self.x -= 1
            elif direction == "l":
                self.drain_battery(factor[2])
                self.y -= 1
            elif direction == "r":
                self.drain_battery(factor[3])
                self.y += 1

        except BatteryException:
            print("Battery ends, sadge")

    def move_seps(self, size, direction):
        self.__iner_task__ = {
                "direction": direction,
                "size": size
                }
        for x in range(size):
            try:
                self.take_photo()
                self.move(direction=direction)
            except BatteryException:
                return False
    
    def calc_dist_to_boundary(self, direction: str) -> int:
        """
        Calculate distance to boudary in selected direction
        """
        distance = 0

        return distance 
        

    def take_photo(self):
        self.drain_battery(0.1)
