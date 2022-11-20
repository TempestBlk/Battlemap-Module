from abc import ABCMeta, abstractmethod
from interface import Interface
from npc import QuartermasterMathias, SeniorResearcherLydia


class Hub(metaclass=ABCMeta):
    title: str

    @abstractmethod
    def main() -> abs:
        pass
    


class NorthWingSZ(Hub):

    title = "North Wing - Sealed Zone"
    desc = "An enclosed area in the north wing of Lab C1. Surviving personel took refuge here when the alarms went on. After a few days they ripped out speaker system, and sent a group to switch lights in the area to local power. Few returned, but they brought with them an outdated fabricator, crude weapons, and stories of creatures roaming the lab."

    
    @staticmethod
    def main(pc):
        inHub = True
        while inHub:
            Interface.clear()
            userInput = input(f"\t--- [{NorthWingSZ.title}] ---\n\n\n{NorthWingSZ.desc}\n\n\n[1] Inventory\n[2] Merchant\n[3] Doctor\n\n[X] Leave\n\n").lower()

            if userInput == "1":
                pass

            elif userInput == "2":
                pass
                QuartermasterMathias.startDialogue(pc)

            elif userInput == "3":
                pass
                SeniorResearcherLydia.startDialogue(pc)
                

            elif userInput == "4":
                pass
                

            elif userInput == "x":
                inHub = False





