class GameOverException(Exception):
    pass


class LoosingReelException(GameOverException):
    """
    exception that is raised when player
    gets 3 skulls
    """
    pass


class NoCreditsException(GameOverException):
    """
    exception that is raised when player
    has lost all money
    """
    pass


class NotEnoughCreditsException(GameOverException):
    """
    exception that is raised when player
    does not have enough money to spin
    """
    pass
