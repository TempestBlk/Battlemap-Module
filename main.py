from gridmap import Actor, Gridmap, Areamap, MapLocation, MapHub, Obstacle, Cache
from hub import NorthWingSZ
from location import PowerStation


gmap = Gridmap(width=15, height=15)


hub = MapHub(icon="SZ", hub=NorthWingSZ)
hub.toMap(gmap, (4,13))


pc = Actor(icon="PC")
pc.toMap(gmap, (3,13))


ps = MapLocation(icon="??", location=PowerStation)
ps.toMap(gmap, (6,7))


# for _ in range(10):
#     o = Obstacle(icon="##")
#     o.toMap(gmap)


# for _ in range(5):
#     c = Cache(icon="C ")
#     c.toMap(gmap)


# for _ in range(4):
#     a = Actor(icon="A ")
#     a.toMap(gmap)


battlemap = Areamap(gmap, pc)
battlemap.start()