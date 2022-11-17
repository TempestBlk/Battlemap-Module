import os
import random
from interface import Interface


class Gridsquare:
    """Coordinate set on map, may contain an actor"""

    def __init__(self, coords:tuple, item:object) -> None:
        self.coords = coords
        self.item = item



class Gridmap:
    """Map of gridsquares in area"""
    mapping: dict[tuple, Gridsquare]

    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height
        self.mapping = {}
        for y in range(height):
            for x in range(width):
                gsquare = Gridsquare((x,y), None)
                self.mapping[(x,y)] = gsquare
    
    def display(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                end = " "
                if x == self.width - 1:
                    end = "\n"
                actor = self.mapping[(x,y)].item
                if actor is None:
                    icon = "."
                else:
                    icon = actor.icon
                print(f"{icon}", end=end)



class Actor:
    def __init__(self, icon:str) -> None:
        self.icon = icon
        self.gmap:Gridmap = None
        self.gsquare:Gridsquare = None

    def enterMap(self, gmap:Gridmap, coords:tuple=None) -> None:
        self.gmap = gmap
        if coords is not None:
            self.gsquare = gmap.mapping[coords]
        else:
            gsquare_full = True
            while gsquare_full:
                self.gsquare = random.choice(gmap.mapping)
                if self.gsquare.item is None:
                    gsquare_full = False
        self.gsquare.item = self
        

    def moveTo(self, coords:tuple) -> None:
        self.gsquare.item = None
        self.gsquare = self.gmap.mapping[coords]
        self.gsquare.item = self



class Direction:
    UP = (0,-1)
    LEFT = (-1,0)
    DOWN = (0,1)
    RIGHT = (1,0)



class Battlemap:

    def __init__(self, gmap:Gridmap, pc:Actor) -> None:
        self.gmap = gmap
        self.pc = pc

    
    def moveActor(self, actor:Actor, direction:tuple):
        cur_coords = actor.gsquare.coords
        new_coords = ((cur_coords[0] + direction[0]), (cur_coords[1] + direction[1]))
        if new_coords[0] < 0 or new_coords[0] > self.gmap.width - 1 or new_coords[1] < 0 or new_coords[1] > self.gmap.height - 1:
            return
        actor.moveTo(new_coords)


    def start(self) -> None:
        Interface.clear()
        print("Entering battle!\n\nActors:\n[P] Player")
        Interface.pressEnter()

        isRunning = True
        while isRunning:
            Interface.clear()
            self.gmap.display()
            user_input = input("\n[W] Up\n[A] Left\n[S] Down\n[D] Right\n[Enter] Wait\n\n").lower()
            if user_input in ["w", "a", "s", "d"]:
                direct_dict = {
                    "w": Direction.UP,
                    "a": Direction.LEFT,
                    "s": Direction.DOWN,
                    "d": Direction.RIGHT
                }
                direction = direct_dict[user_input]
                self.moveActor(self.pc, direction)
                