import sys
from interface import Interface
from lifeforms import PlayerCharacter


class CustomError(Exception):
    pass



class QuietError(CustomError):
    pass



class QuitGame(QuietError):
    """
    Exception raised when user chooses 'Quit'
    """

    def __init__(self, pc:PlayerCharacter) -> None:
        msg = "player chose 'Quit'"
        Interface.clear()
        print(f"---[Quitting Game]---\n")
        Interface.characterInfo(pc, stats=True)
        print("\n\nBut you were so close!\n\n")
        super().__init__(msg)



class PlayerDied(QuietError):
    """
    Exception raised when player character dies
    """

    def __init__(self, pc:PlayerCharacter) -> None:
        msg = "player character died"
        Interface.clear()
        print(f"---[Player Died]---\n")
        Interface.characterInfo(pc, stats=True)
        print("\n\nBut you were so close!\n\n")
        super().__init__(msg)



def quiet_hook(kind, message, traceback):
    if QuietError in kind.__bases__:
        print('{0}: {1}'.format(kind.__name__, message))  # Only print Error Type and Message
    else:
        sys.__excepthook__(kind, message, traceback)  # Print Error Type, Message and Traceback


sys.excepthook = quiet_hook