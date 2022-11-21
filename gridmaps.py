import random


class Gridsquare:
    """
    A Gridsquare is created for every coordinate point in its Gridmap.\n
    May contain a MapEntity.
    """

    def __init__(self, coords:tuple, within) -> None:
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