from dataclasses import dataclass, field
import random
from utils import Directions, Distributions
import numpy as np

@dataclass()
class Map:
    size: int
    wind_size: int
    photo_radius: int
    wind_distribution: Distributions
    overlap: float
    beg: int = field(init=False)  # beg - beginning of wind stream
    direction: str = field(init=False)

    def __post_init__(self):
        self.beg = random.randint(0, self.size - self.wind_size)  # select random begining of wind stream
        self.wind_direction = random.choice([Directions.LEFT, Directions.RIGHT])
        self.drone_map = None
        match self.wind_direction:  # assign symbol for futher plot creation
            case Directions.LEFT:
                self.wind_direction_symbol = "<"
            case Directions.RIGHT:
                self.wind_direction_symbol = ">"
            case _:
                raise ValueError
        self.wind_table_generator()  # CREATE AN (x,y) -> val relation

    def wind_table_generator(self):
        match self.wind_distribution:
            case Distributions.NORMAL:
                self.__normal_distrib_wind_generator()

            case Distributions.UNIFORM:
                pass

            case Distributions.FIXED_VALUE:
                self.__fixed_val_wind_generator()

    def __normal_distrib_wind_parser(self, distrib: list) -> list:
        """
        Helper method to parse normal Distribution to simulate wind
        """
        data = sorted([(abs(x)).__round__(1) for x in distrib],reverse=True)
        wind_data = [data[0]]
        for idx,elem in enumerate(data):
            if idx == 0:
                continue
            elif idx%2 == 0:
                wind_data = [elem, *wind_data]
            else:
                wind_data.append(elem)
        return wind_data
    
    def __normal_distrib_wind_generator(self) -> None:
        """
        generate wind table from fixed value (in this case binary)
        """
        # wind table
        self.wind_table = []
        
        # normal distrib config vars, i should move this outside
        MU = 1
        SIGMA = 0.5

        flag = False # flag for signaling row with wind

        
        if len(self.wind_table) != 0:
            raise ValueError

        wind_distribution = self.__normal_distrib_wind_parser(list(np.random.normal(MU, SIGMA, self.wind_size+1)))
        i = 0 # indicator
        # print(f"wind_size = {self.wind_size}\nlen() = {len(wind_distribution)}")
        # print(f"Beg: {self.beg}\nEnd: {self.beg+self.wind_size}")
        for y in range(self.size): # first iterating over rows
            tmp = []
            for x in range(self.size):
                if self.beg <= y <= self.beg + self.wind_size:
                    flag = True #set flag to true to trigger i
                    tmp.append([x, y, wind_distribution[i]]) # generate abs of wind Distribution 
                else:
                    tmp.append([x, y, 0])
            if flag:
                i += 1
                # print(f"Row {y} - used")
                flag = False


            self.wind_table.append(tmp)


    def __fixed_val_wind_generator(self) -> None:
        """
        generate wind table from normal Distribution (in this case in range 0.1 - 1.5)
        """
        
        self.wind_table = []
        for x in range(self.size):
            tmp = []
            for y in range(self.size):
                if self.beg <= y <= self.beg + self.wind_size:
                    tmp.append([x, y, 1])
                else:
                    tmp.append([x, y, 0])
            self.wind_table.append(tmp)

    def get_wind_val(self, x, y) -> int:
        for row in self.wind_table:
            for point in row:
                if (point[0] == x) and (point[1] == y):
                    return point[2]
        raise ValueError("Point not found")

    def upload_drone_movent(self, history: list):
        self.drone_map = history

    def show_map(self, marked_drone_path: bool) -> None:
        import matplotlib.pyplot as plt

        # perform base drawing of generated map

        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax1 = fig.add_subplot(111)

        for row in self.wind_table:
            for point in row:
                if point[2] != 0:
                    ax1.plot(point[0], point[1], color="green", marker=self.wind_direction_symbol)
                else:
                    ax1.plot(point[0], point[1], color="gray", marker="o")

        ax1.plot(0, 0, color="yellow", marker="o")  # adding start point to the map

        if marked_drone_path and self.drone_map:
            for point in self.drone_map:
                ax1.plot(point[0], point[1], color="yellow", marker="o")
            pass

        plt.show()


if __name__ == "__main__":
    map = Map(
        size=50,
        wind_size=20,
        photo_radius=3,
        overlap=0.5,
        wind_distribution=Distributions.FIXED_VALUE
    )
    map.show_map(False)
