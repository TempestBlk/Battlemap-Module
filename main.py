from battlemap import Actor, Location, Gridmap, Battlemap


gmap = Gridmap(width=10, height=10)

pc = Actor(icon="PC")
pc.enterMap(gmap)

for _ in range(10):
    l = Location(icon="L1")
    l.enterMap(gmap)

for _ in range(10):
    a = Actor(icon="A1")
    a.enterMap(gmap)

battlemap = Battlemap(gmap, pc)
battlemap.start()