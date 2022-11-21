class Levelup():
    level_list = {
        1: 0,
        2: 10,
        3: 25,
        4: 40,
        5: 65,
        6: 999
    }


    @classmethod
    def check(self, lifeform):
        from interface import Interface
        checking = True
        while checking:
            if lifeform.xp >= Levelup.level_list[(lifeform.level + 1)]:
                lifeform.level += 1

                lifeform.max_hp += 2
                lifeform.hp += 2
                
                lifeform.xp -= Levelup.level_list[(lifeform.level)]
                Interface.levelupMessage(lifeform)
            else:
                checking = False