__all__ = ["Game"]

from .exceptions import NotEnoughCreditsException, NoCreditsException
from .reel import Reels, Reel


class Game:
    def __init__(self, inital_credits: int, go_cost: int) -> None:
        """
        create a game object

            :param inital_credits: how many credits the
                                   player starts with
            :param go_cost: the cost for a spin
        """
        self.__go_cost = go_cost
        self.__inital_credits = inital_credits
        self.__curr_credits = self.__inital_credits
        self.__credits_won = 0
        self.__game_reels = Reels()

    def reset(self) -> None:
        """
        resets the game state to defaults
        """
        self.__curr_credits = self.__inital_credits
        self.__credits_won = 0
        self.__game_reels.to_default()

    def spin(self) -> None:
        """
        spins the reels

            :raises NotEnoughCreditsException: when there are not
                                               enough credits for a go
        """
        if self.curr_credits < self.go_cost:
            raise NotEnoughCreditsException()
        self.__curr_credits -= self.go_cost
        self.__game_reels.spin()

    def calc_spin(self) -> None:
        """
        calculates the reels
            :raises NoCreditsException: when there are no credits left
            :raises LoosingReelException: when a game is lost
                                          because of a reel match
        """
        self.__credits_won = self.__game_reels.calc_reels()
        self.__curr_credits += self.__credits_won
        if self.__curr_credits < 0:
            raise NoCreditsException()

    @property
    def go_cost(self) -> int:
        return self.__go_cost

    @property
    def inital_credits(self) -> int:
        return self.__inital_credits

    @property
    def curr_credits(self) -> int:
        return self.__curr_credits

    @property
    def credits_won(self) -> int:
        return self.__credits_won

    @property
    def reels(self) -> list[Reel]:
        return self.__game_reels.reels
