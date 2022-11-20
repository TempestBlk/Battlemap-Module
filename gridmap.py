from abc import abstractmethod
import random
from interface import Interface
from hub import Hub
from location import Location, PowerStation


class Gridsquare:
    """
    A Gridsquare is created for every coordinate point in its Gridmap.\n
    May contain a MapEntity.
    """

    def __init__(self, coords:tuple, within:object) -> None:
        self.coords = coords
        self.within = within



class Gridmap:
    """
    Data structure containing a two dimensional grid of Gridsquares.\n
    Handles displaying map in terminal.
    """
    UP = (0,-1)
    LEFT = (-1,0)
    DOWN = (0,1)
    RIGHT = (1,0)

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
                actor = self.mapping[(x,y)].within
                if actor is None:
                    icon = ".."
                else:
                    icon = actor.icon
                print(f"{icon}", end=end)



class MapEntity:
    """
    Object which inhabits a square on the map.
    May be a Location or Actor.
    """

    def __init__(self, icon:str) -> None:
        self.icon = icon
        self.gmap:Gridmap = None
        self.gsquare:Gridsquare = None
    

    def toMap(self, gmap:Gridmap, coords:tuple=None) -> None:
        self.gmap = gmap
        if coords is not None:
            new_gsquare = gmap.mapping[coords]
        else:
            gsquare_full = True
            while gsquare_full:
                new_x = random.randint(0, (self.gmap.width - 1))
                new_y = random.randint(0, (self.gmap.height - 1))
                new_gsquare = self.gmap.mapping[(new_x, new_y)]
                if new_gsquare.within is None:
                    gsquare_full = False
        self.gsquare = new_gsquare
        self.gsquare.within = self

    

class Obstacle(MapEntity):
    """
    An obstacle on the areamap.
    Cannot move through or interact with.
    """



class MapLocation(MapEntity):
    """
    A Location to explore, visible on the Areamap.
    """

    def __init__(self, icon:str, location:Location=None) -> None:
        super().__init__(icon)
        self.location = location
        self.visited = False


    def enter(self, actor:object):
        if self.visited is False:
            self.visited = True
            self.icon = "PS"
        self.location.explore()
        



class Actor(MapEntity):
    """
    Lifeform moving through a map.
    """

    def __init__(self, icon: str) -> None:
        super().__init__(icon)
        self.gold_flakes = 0
        self.max_hp = 15
        self.hp = self.max_hp
    
    def moveTo(self, coords:tuple) -> None:
        new_gsquare = self.gmap.mapping[coords]

        if isinstance(new_gsquare.within, Obstacle):
            return
        
        elif isinstance(new_gsquare.within, Actor):
            hp_cost = random.randint(1,3)
            self.hp -= hp_cost
            Interface.clear()
            print(f"Encountered a lifeform!\nLost {hp_cost} hp.")
            if self.hp < 1:
                print(f"You died!")
                Interface.pressEnter()
                return
            Interface.pressEnter()

        elif isinstance(new_gsquare.within, MapHub):
            new_gsquare.within.hub.main(self)
            return

        elif isinstance(new_gsquare.within, Cache):
            new_gsquare.within.enter(self)

        elif isinstance(new_gsquare.within, MapLocation):
            new_gsquare.within.enter(self)
            return

        self.gsquare.within = None
        self.gsquare = new_gsquare
        new_gsquare.within = self



class MapHub(MapLocation):
    """
    Entrance to Hub Location from Areamap
    """
    def __init__(self, icon: str, hub:Hub) -> None:
        super().__init__(icon)
        self.hub = hub



class Cache(MapLocation):
    def enter(self, actor):
        reward = random.randint(1,13)
        actor.gold_flakes += reward

        Interface.clear()
        print(f"Found {reward} gold flakes")
        Interface.pressEnter()



class Areamap:
    """
    todo desc
    """

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
        # print("Entering battle!\n\nActors:\n[P] Player")
        # Interface.pressEnter()

        isRunning = True
        while isRunning:
            Interface.clear()
            self.gmap.display()
            user_input = input(f"\n\nHp: {self.pc.hp}/{self.pc.max_hp}\nGold Flakes: {self.pc.gold_flakes}\n\n[W] Up\n[A] Left\n[S] Down\n[D] Right\n\n[Enter] Wait\n[X] Quit\n\n").lower()
            if user_input in ["w", "a", "s", "d"]:
                direct_dict = {
                    "w": self.gmap.UP,
                    "a": self.gmap.LEFT,
                    "s": self.gmap.DOWN,
                    "d": self.gmap.RIGHT
                }
                direction = direct_dict[user_input]
                self.moveActor(self.pc, direction)
                if self.pc.hp < 1:
                    isRunning = False
            elif user_input == "x":
                Interface.clear()
                print("Ending the simulation...")
                # Interface.pressEnter()
                isRunning = False