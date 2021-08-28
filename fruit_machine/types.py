"""
custom types
"""
__all__ = ["IconNames", "AppSettings"]

from dataclasses import dataclass
from enum import IntEnum, auto, unique


@unique
class IconNames(IntEnum):
    """
    Enums for Icon Names
    """
    COMBINATIONS = auto()
    SKULL = auto()
    BELL = auto()
    CHERRY = auto()
    LEMON = auto()
    ORANGE = auto()
    STAR = auto()


@dataclass
class AppSettings:
    """
    Holds the app settings
    """
    starting_credits: int
    go_cost: int
    image_scale: int
    assets: dict
