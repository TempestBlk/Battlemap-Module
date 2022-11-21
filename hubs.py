from abc import ABCMeta, abstractmethod
from errors import QuitGame
from interface import Interface
from inventory import Inventory
from lifeforms import PlayerCharacter
from npcs import QuartermasterMathias, SeniorResearcherLydia


class Hub(metaclass=ABCMeta):
    """
    """

    title: str
    desc: str

    @abstractmethod
    def approach(pg) -> None:
        pass


    @abstractmethod
    def enter(pg) -> None:
        pass
    


class NorthWingSZ(Hub):
    """
    """

    title = "North Wing - Sealed Zone"
    desc = "An enclosed area in the north wing of Lab C1. Surviving personel took refuge here when the alarms went on. After a few days they ripped out speaker system, and sent a group to switch lights in the area to local power. Few returned, but they brought with them an outdated fabricator, crude weapons, and stories of creatures roaming the lab."

    
    @classmethod
    def hubHeader(self, pc):
        Interface.clear()
        print(f"\t--- [{self.title}] ---\n\n\n{self.desc}\n")
        Interface.characterInfo(pc)


    @classmethod
    def approach(self, pg):
        self.enter(pg)


    @classmethod
    def enter(self, pg):

        inHub = True
        while inHub:
            self.hubHeader(pg.pc)
            userInput = input(f"\n\n[1] Inventory\n[2] Merchant\n[3] Doctor\n[4] Leave \n\n[X] Quit\n\n").lower()

            if userInput == "1":
                Inventory.open(pg.pc)

            elif userInput == "2":
                QuartermasterMathias.startDialogue(pg.pc)

            elif userInput == "3":
                pass
                SeniorResearcherLydia.startDialogue(pg.pc)
                

            elif userInput == "4":
                inHub = False
                

            elif userInput == "x":
                raise QuitGame(pg.pc)