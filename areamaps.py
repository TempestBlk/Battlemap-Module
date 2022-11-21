import random
from abc import ABCMeta, abstractmethod
from errors import QuitGame
from interface import Interface
from items import Weapon
from lifeforms import Lifeform, PlayerCharacter, Mindless
from gridmaps import Gridmap, MapEntity
from hubs import Hub, NorthWingSZ
from encounters import Encounter, EncounterBuilder


class Obstacle(MapEntity):
    """
    An obstacle on the areamap.
    Cannot move through or interact with.
    """


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



class EnemyGroup(MapActor):
    """
    TODO:
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


    def encounter(self, pg:PlayerGroup) -> bool:
        encounter = Encounter(pg.pc, self.enemies, pg.allies)
        encounter.runEncounter()



class Location(metaclass=ABCMeta):
    """
    A Location to explore, visible on the Areamap.
    """

    @abstractmethod
    def approach(self, pg:PlayerGroup) -> None:
        pass

    
    @abstractmethod
    def enter(self, pg:PlayerGroup) -> None:
        pass



class Cache(Location):
    """
    TODO:
    """

    @classmethod
    def approach(self, pg:PlayerGroup):
        reward = random.randint(1,13)
        pg.pc.gold_flakes += reward

        Interface.clear()
        print(f"Found {reward} gold flakes")
        Interface.pressEnter()



class PowerStation(Location):
    """
    TODO: docstring
    """

    @classmethod
    def approach(self, pg:PlayerGroup) -> None:
        self.enter(pg)


    @classmethod
    def enter(self, pg:PlayerGroup) -> None:
        encounter = EncounterBuilder.build(pg.pc, 2, allies=pg.allies)
        encounter.runEncounter()



class MapLocation(MapEntity):
    """
    TODO: docstring
    """
    hidden:bool
    invis_icon:str

    def __init__(self, icon:str, location:Location, hidden=False) -> None:
        self.hidden = hidden
        if hidden is True:
            self.invis_icon = icon
            icon = "??"
        super().__init__(icon)
        self.location = location
        self.hidden = hidden
        

    def approach(self, pg:PlayerGroup) -> None:
        if self.hidden is True:
            self.hidden = False
            self.icon = self.invis_icon
        self.location.approach(pg)



class MapHub(MapLocation):
    """
    Entrance to Hub Location from Areamap
    """

    def __init__(self, icon: str, hub:Hub) -> None:
        super().__init__(icon, hub)



class MapEvent(MapLocation):
    """
    TODO: docstring
    """

    def __init__(self, icon: str, location: Location) -> None:
        super().__init__(icon, location)



class Area:
    """
    TODO:
    """

    def __init__(self, gmap:Gridmap, pg:PlayerGroup) -> None:
        self.gmap = gmap
        self.pg = pg
        self.pc = pg.pc

    
    def movePlayerGroup(self, pg:PlayerGroup, direction:tuple):
        cur_coords = pg.gsquare.coords
        new_coords = ((cur_coords[0] + direction[0]), (cur_coords[1] + direction[1]))
        if new_coords[0] < 0 or new_coords[0] > self.gmap.width - 1 or new_coords[1] < 0 or new_coords[1] > self.gmap.height - 1:
            return

        new_gsquare = self.gmap.mapping[new_coords]
        if isinstance(new_gsquare.within, Obstacle):
            return
        elif isinstance(new_gsquare.within, EnemyGroup):
            new_gsquare.within.encounter(self.pg)
        elif isinstance(new_gsquare.within, MapEvent):
            new_gsquare.within.approach(self.pg)
        elif isinstance(new_gsquare.within, MapLocation):
            new_gsquare.within.approach(self.pg)
            return
        


        self.pg.gsquare.within = None
        self.pg.gsquare = new_gsquare
        new_gsquare.within = self.pg


    def start(self, start_hub:MapHub=None) -> None:
        if start_hub is not None:
            start_hub.location.approach(self.pg)


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
                self.movePlayerGroup(self.pg, direction)
                if self.pg.hp < 1:
                    isRunning = False
            elif user_input == "x":
                raise QuitGame(self.pc)
                # isRunning = False



class LabC1NorthWing(Area):
    """
    TODO:
    """

    @classmethod
    def build(self, pc):
        gmap = Gridmap(width=15, height=15)


        hub = MapHub(icon="SZ", hub=NorthWingSZ)
        hub.toMap(gmap, (4,13))


        pg = PlayerGroup(pc)
        pg.toMap(gmap, (3,13))


        ps = MapLocation(icon="PS", location=PowerStation, hidden=True)
        ps.toMap(gmap, (6,7))

        for _ in range(3):
            eg = EnemyGroup(EnemyGroup.LONE_MINDLESS, icon="1M")
            eg.toMap(gmap)

        for _ in range(1):
            eg = EnemyGroup(EnemyGroup.LIGHT_MINDLESS, icon="2M")
            eg.toMap(gmap)


        for _ in range(2):
            o = Obstacle(icon="##")
            o.toMap(gmap)


        for _ in range(3):
            c = MapEvent(icon="C ", location=Cache)
            c.toMap(gmap)


        area = self(gmap, pg)
        area.start(start_hub=hub)