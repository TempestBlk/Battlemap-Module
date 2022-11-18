import random
from interface import Interface


class Gridsquare:
    """Coordinate set on map, may contain an actor"""

    def __init__(self, coords:tuple, within:object) -> None:
        self.coords = coords
        self.within = within



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
                actor = self.mapping[(x,y)].within
                if actor is None:
                    icon = ".."
                else:
                    icon = actor.icon
                print(f"{icon}", end=end)



class Entity:
    """Object inhabiting a square on grip"""

    def __init__(self, icon:str) -> None:
        self.icon = icon
        self.gmap:Gridmap = None
        self.gsquare:Gridsquare = None
    

    def enterMap(self, gmap:Gridmap, coords:tuple=None) -> None:
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



class Location(Entity):
    """Explorable area inhabiting a square on grid"""
    def explore(self, actor):
        reward = random.randint(1,13)
        actor.gold_flakes += reward

        Interface.clear()
        print(f"Found {reward} gold flakes")
        Interface.pressEnter()


class Actor(Entity):
    """Lifeform moving through grid"""
    def __init__(self, icon: str) -> None:
        super().__init__(icon)
        self.gold_flakes = 0
        self.max_hp = 15
        self.hp = self.max_hp
    
    def moveTo(self, coords:tuple) -> None:
        new_gsquare = self.gmap.mapping[coords]

        if isinstance(new_gsquare.within, Actor):
            hp_cost = random.randint(1,3)
            self.hp -= hp_cost
            Interface.clear()
            print(f"Encountered a lifeform!\nLost {hp_cost} hp.")
            if self.hp < 1:
                print(f"You died!")
                Interface.pressEnter()
                return
            Interface.pressEnter()

        if isinstance(new_gsquare.within, Location):
            new_gsquare.within.explore(self)
        self.gsquare.within = None
        self.gsquare = new_gsquare
        new_gsquare.within = self        



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
            user_input = input(f"\n\nHp: {self.pc.hp}/{self.pc.max_hp}\nGold Flakes: {self.pc.gold_flakes}\n\n[W] Up\n[A] Left\n[S] Down\n[D] Right\n\n[Enter] Wait\n[X] End Simulation\n\n").lower()
            if user_input in ["w", "a", "s", "d"]:
                direct_dict = {
                    "w": Direction.UP,
                    "a": Direction.LEFT,
                    "s": Direction.DOWN,
                    "d": Direction.RIGHT
                }
                direction = direct_dict[user_input]
                self.moveActor(self.pc, direction)
                if self.pc.hp < 1:
                    isRunning = False
            elif user_input == "x":
                Interface.clear()
                print("Ending the simulation...")
                Interface.pressEnter()
                isRunning = False