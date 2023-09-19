from enum import Enum


class GameType(str, Enum):
    BOL_DEFAULT = "bol_default"
    WIKIPEDIA_VERSION = "wikipedia_version"


class Player(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2

    def __str__(self):
        return self.name


class PitType(str, Enum):
    SMALL = "small"
    LARGE = "large"
