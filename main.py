from areas import Gridmap, MapLocation, PlayerGroup, EnemyGroup, MapHub, Obstacle, Cache, Areamap
from hubs import NorthWingSZ
from locations import PowerStation
from lifeforms import PlayerCharacter
from items import Weapon, Wearable


pc = PlayerCharacter("Jr Researcher Krycek", "researcher") # NOTE: "if save file, load pc from file, else start newgame"
starting_items = [Weapon(Weapon.metal_pipe), Weapon(Weapon.shiv), Wearable(Wearable.junior_researcher_coat), Wearable(Wearable.tf5_fireteam_vest), Weapon(Weapon.f_collective_solspear)]
pc.inventory += starting_items
pc.equipWearable(Wearable(Wearable.torn_clothes))


gmap = Gridmap(width=15, height=15)


hub = MapHub(icon="SZ", hub=NorthWingSZ)
hub.toMap(gmap, (4,13))


pc = PlayerGroup(pc)
pc.toMap(gmap, (3,13))


ps = MapLocation(icon="??", location=PowerStation)
ps.toMap(gmap, (6,7))

for _ in range(5):
    eg = EnemyGroup(EnemyGroup.LONE_MINDLESS, icon="1M")
    eg.toMap(gmap)

for _ in range(2):
    eg = EnemyGroup(EnemyGroup.LIGHT_MINDLESS, icon="2M")
    eg.toMap(gmap)


# for _ in range(10):
#     o = Obstacle(icon="##")
#     o.toMap(gmap)


# for _ in range(5):
#     c = Cache(icon="C ")
#     c.toMap(gmap)


# for _ in range(4):
#     a = Actor(icon="A ")
#     a.toMap(gmap)


areamap = Areamap(gmap, pc)
areamap.start(start_hub=hub)