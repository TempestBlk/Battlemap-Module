from battlemap import Actor, Gridmap, Battlemap


gmap = Gridmap(width=20, height=20)

pc = Actor(icon="P")
pc.enterMap(gmap, (0,0))

battlemap = Battlemap(gmap, pc)
battlemap.start()