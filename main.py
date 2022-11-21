from lifeforms import PlayerCharacter
from items import Weapon, Wearable
from areamaps import LabC1NorthWing


def buildPC() -> PlayerCharacter:
    pc = PlayerCharacter("Jr Researcher Krycek", "researcher") # NOTE: "if save file, load pc from file, else start newgame"
    starting_items = [Weapon(Weapon.metal_pipe), Weapon(Weapon.shiv), Wearable(Wearable.junior_researcher_coat), Wearable(Wearable.tf5_fireteam_vest), Weapon(Weapon.f_collective_solspear)]
    pc.inventory += starting_items
    pc.equipWearable(Wearable(Wearable.torn_clothes))
    return pc
    

def newGame(pc:PlayerCharacter):
    LabC1NorthWing.build(pc)


if __name__ == "__main__":
    pc = buildPC()
    newGame(pc)