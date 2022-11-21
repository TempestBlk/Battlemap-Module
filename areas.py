from abc import abstractmethod
import random
from interface import Interface
from hubs import Hub
from locations import Location
from lifeforms import Lifeform, PlayerCharacter, Mindless
from items import Weapon
from encounters import Encounter


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
    May be a Location or MapActor.
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
        


class MapActor(MapEntity):
    """
    Lifeform moving through a map.
    """

    def __init__(self, icon:str) -> None:
        super().__init__(icon)



class PlayerGroup(MapActor):
    def __init__(self, pc:PlayerCharacter, allies:list[Lifeform]=None, icon:str="PC") -> None:
        super().__init__(icon)
        self.pc = pc
        self.allies = allies
        self.gold_flakes = 0
        self.max_hp = 15
        self.hp = self.max_hp


    def moveTo(self, coords:tuple) -> None:
        new_gsquare = self.gmap.mapping[coords]

        if isinstance(new_gsquare.within, Obstacle):
            return

        elif isinstance(new_gsquare.within, EnemyGroup):
            new_gsquare.within.encounter(self.pc)

        elif isinstance(new_gsquare.within, MapHub):
            new_gsquare.within.hub.main(self.pc)
            return

        elif isinstance(new_gsquare.within, Cache):
            new_gsquare.within.enter(self.pc)

        elif isinstance(new_gsquare.within, MapLocation):
            new_gsquare.within.enter(self.pc)
            return

        self.gsquare.within = None
        self.gsquare = new_gsquare
        new_gsquare.within = self



class EnemyGroup(MapActor):
    """
    """

    LONE_MINDLESS = [[Mindless, "Mindless-1"]]
    LIGHT_MINDLESS = [[Mindless, "Mindless-1"], [Mindless, "Mindless-2"]]


    def __init__(self, group:list[list], icon:str="HG") -> None:
        super().__init__(icon)

        self.enemies = []
        for enemy in group:
            enemy_class = enemy[0]
            lifeform:Lifeform = enemy_class(enemy[1])
            if len(enemy) > 2:
                lifeform.equipWeapon(Weapon(enemy[2]))
            self.enemies.append(lifeform)


    def encounter(self, pc, allies=None):
        new_encounter = Encounter(pc, self.enemies, allies)
        return new_encounter



class MapHub(MapLocation):
    """
    Entrance to Hub Location from Areamap
    """
    def __init__(self, icon: str, hub:Hub) -> None:
        super().__init__(icon)
        self.hub = hub



class Cache(MapLocation):
    def enter(self, actor:PlayerCharacter):
        reward = random.randint(1,13)
        actor.gold_flakes += reward

        Interface.clear()
        print(f"Found {reward} gold flakes")
        Interface.pressEnter()



class Areamap:
    """
    todo desc
    """

    def __init__(self, gmap:Gridmap, pg:PlayerGroup) -> None:
        self.gmap = gmap
        self.pg = pg
        self.pc = pg.pc

    
    def moveMapActor(self, actor:MapActor, direction:tuple):
        cur_coords = actor.gsquare.coords
        new_coords = ((cur_coords[0] + direction[0]), (cur_coords[1] + direction[1]))
        if new_coords[0] < 0 or new_coords[0] > self.gmap.width - 1 or new_coords[1] < 0 or new_coords[1] > self.gmap.height - 1:
            return
        actor.moveTo(new_coords)


    def start(self, start_hub:MapHub=None) -> None:
        if start_hub is not None:
            start_hub.hub.main(self.pc)

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
                self.moveMapActor(self.pg, direction)
                if self.pg.hp < 1:
                    isRunning = False
            elif user_input == "x":
                Interface.clear()
                print("Ending the simulation...")
                # Interface.pressEnter()
                isRunning = False