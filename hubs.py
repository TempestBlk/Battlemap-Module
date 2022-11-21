from abc import ABCMeta, abstractmethod
from interface import Interface
from npcs import QuartermasterMathias, SeniorResearcherLydia
from inventory import Inventory


class Hub(metaclass=ABCMeta):
    """
    """

    title: str


    @abstractmethod
    def main() -> abs:
        pass
    


class NorthWingSZ(Hub):
    """
    """

    from lifeforms import PlayerCharacter

    title = "North Wing - Sealed Zone"
    desc = "An enclosed area in the north wing of Lab C1. Surviving personel took refuge here when the alarms went on. After a few days they ripped out speaker system, and sent a group to switch lights in the area to local power. Few returned, but they brought with them an outdated fabricator, crude weapons, and stories of creatures roaming the lab."

    
    @classmethod
    def hubHeader(self, pc:PlayerCharacter):
        Interface.clear()
        print(f"\t--- [{self.title}] ---\n\n\n{self.desc}\n")
        Interface.characterInfo(pc)


    @classmethod
    def main(self, pc:PlayerCharacter):
        inHub = True
        while inHub:
            self.hubHeader(pc)
            userInput = input(f"\n\n[1] Inventory\n[2] Merchant\n[3] Doctor\n\n[X] Leave\n\n").lower()

            if userInput == "1":
                Inventory.open(pc)

            elif userInput == "2":
                QuartermasterMathias.startDialogue(pc)

            elif userInput == "3":
                pass
                SeniorResearcherLydia.startDialogue(pc)
                

            elif userInput == "4":
                pass
                

            elif userInput == "x":
                inHub = False