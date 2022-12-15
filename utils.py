from enum import Enum

class Directions(Enum):
    UP = "u"
    DOWN = "d"
    LEFT = "l"
    RIGHT = "r"

class Distributions(Enum):
    NORMAL = 1
    UNIFORM = 2
    FIXED_VALUE = 3

