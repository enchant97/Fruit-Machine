"""
the game reels
"""
__all__ = ["Reel", "Reels"]

from collections import Counter
from random import choices

from .exceptions import LoosingReelException
from .types import IconNames


class Reel:
    """
    The game reel class that
    contains each column for a row
    """
    __choices = (
        IconNames.BELL,
        IconNames.CHERRY,
        IconNames.LEMON,
        IconNames.ORANGE,
        IconNames.STAR,
        IconNames.SKULL
    )
    __weights = (1, 3, 3, 3, 3, 5)

    def __init__(self):
        self.__reel = [IconNames.BELL, IconNames.BELL, IconNames.BELL]

    def calc_row(self) -> int:
        """
        calculates the credits gained/lost on reel

            :raises LoosingReelException: if player got 3 skulls
            :return: the credits gained/lost
        """
        counts = Counter(self.__reel).most_common(1)[0]
        if counts[1] == 1:
            return 0
        elif counts[0] == IconNames.SKULL:
            if counts[1] == 3:
                raise LoosingReelException()
            elif counts[1] == 2:
                return -100
        elif counts[0] == IconNames.BELL and counts[1] == 3:
            return 500
        elif counts[1] == 3:
            return 100
        elif counts[1] == 2:
            return 50

    def __spin_reel_col(self):
        return choices(self.__choices, self.__weights)[0]

    def spin(self):
        """
        spins the row, using choices and
        weights for randomly picking
        """
        self.__reel = [self.__spin_reel_col() for _ in range(3)]

    @property
    def reel(self):
        return self.__reel


class Reels:
    """
    the game reels class that
    contains each row for the reel
    """
    __reels: list[Reel] = None

    def __init__(self):
        self.to_default()

    def to_default(self):
        """
        reset the reels to default values
        """
        self.__reels = [Reel() for _ in range(3)]

    def calc_reels(self) -> int:
        """
        calculates the credits gained/lost on all reels

            :raises LoosingReelException: if player got 3 skulls
            :return: the credits gained/lost
        """
        credits_ = 0
        for reel in self.__reels:
            reel_value = reel.calc_row()
            credits_ += reel_value
        return credits_

    def spin(self):
        """
        spins all the reels
        """
        for reel in self.__reels:
            reel.spin()

    @property
    def reels(self):
        return self.__reels
