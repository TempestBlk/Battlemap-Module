from attacks import Attack


class Item():
    name:str
    durability:int
    basePrice:int

    def build(self, item_type, pattern):
        if item_type == 'weapon':
            item = Weapon(pattern)
        elif item_type == 'wearable':
            item = Wearable(pattern)
        return item



class Weapon(Item):
    shiv = {
        "id": "shiv",
        "name": "Shiv",
        "durability": 15,
        "basePrice": 4,
        "attacks": [Attack.shiv_stab]
    }
    
    metal_pipe = {
        "id": "metal_pipe",
        "name": "Metal Pipe",
        "durability": 30,
        "basePrice": 8,
        "attacks": [Attack.metal_pipe_slam, Attack.metal_pipe_swing]
    }

    bondprint_sabre = {
        "id": "bondprint_sabre",
        "name": "Bondprint Sabre",
        "durability": 75,
        "basePrice": 65,
        "attacks": [Attack.bondprint_sabre_slash, Attack.bondprint_sabre_cleave]
    }

    f_collective_solspear = {
        "id": "f_collective_solspear",
        "name": "F Collective Solspear",
        "durability": 1200,
        "basePrice": 2200,
        "attacks": [Attack.f_collective_solspear_impale]
    }


    def __init__(self, weapon):
        self.id = weapon['id']
        self.name:str = weapon['name']
        self.max_durability:int = weapon['durability']
        self.durability:int = self.max_durability
        self.basePrice:int = weapon['basePrice']
        self.attacks:list[Attack] = weapon['attacks']



class Wearable(Item):
    # protection for parts --> [slash, pierce, blunt]
    # onEquip add protection scores to lifeform stats
    # every 5 protection = 1 damage reduction
    # every 10 protection = -1 to hit

    torn_clothes = {
        "id": "torn_clothes",
        "name": "Torn Clothes",
        "layer": "under",
        "durability": 50,
        "basePrice": 5,
        "dcMod": 0,
        "protection": {
            "torso": [1,1,0],
            "stomach": [1,1,0],
            "arms": [1,0,0],
            "legs": [1,0,0]
        }
    }

    researcher_garb = {
        "id": "researcher_garb",
        "name": "Researcher Garb",
        "layer": "under",
        "durability": 120,
        "basePrice": 25,
        "dcMod": 0,
        "protection": {
            "torso": [2,1,1],
            "stomach": [2,1,1],
            "arms": [2,1,1],
            "legs": [1,1,0]
        }
    }

    tf5_fieldwear = {
        "id": "tf5_fieldwear",
        "name": "TF-5 Fieldwear",
        "layer": "under",
        "durability": 250,
        "basePrice": 65,
        "dcMod": 1,
        "protection": {
            "torso": [3,2,1],
            "stomach": [2,2,1],
            "arms": [1,1,1],
            "legs": [1,1,1]
        }
    }

    junior_researcher_coat = {
        "id": "junior_researcher_coat",
        "name": "Junior Researcher Coat",
        "layer": "outer",
        "durability": 180,
        "basePrice": 55,
        "dcMod": 0,
        "protection": {
            "torso": [4,2,1],
            "stomach": [3,2,1],
            "arms": [3,2,1],
        }
    }

    modified_researcher_coat = {
        "id": "modified_researcher_coat",
        "name": "Modified Researcher Coat",
        "slot": "outer",
        "durability": 250,
        "basePrice": 160,
        "dcMod": 0,
        "protection": {
            "torso": [8,3,2],
            "stomach": [4,3,2],
            "arms": [4,2,2],
        }
    }

    gensec_patrol_vest = {
        "id": "gensec_patrol_vest",
        "name": "Gen-Sec Patrol Vest",
        "layer": "vest",
        "durability": 350,
        "basePrice": 200,
        "dcMod": 0,
        "protection": {
            "torso": [15,25,4],
            "stomach": [5,10,4],
        }
    }

    tf5_fireteam_vest = {
        "id": "tf5_fireteam_vest",
        "name": "TF-5 Fireteam Vest",
        "layer": "vest",
        "durability": 600,
        "basePrice": 400,
        "dcMod": 0,
        "protection": {
            "torso": [22,32,6],
            "stomach": [8,14,6],
        }
    }

    tf5_plate_carrier = {
        "id": "tf5_plate_carrier",
        "name": "TF-5 Plate Carrier",
        "pattern": "tf5",
        "plates": "tf5-c3",
        "layer": "plate_carrier",
        "durability": 800,
        "basePrice": 1200,
        "dcMod": -2,
        "protection": {
            "torso": [35,50,20],
            "stomach": [15,25,15],
        }
    }

    tf12_castle_carrier = {
        "id": "tf12_castle_carrier",
        "name": "TF-12 Castle Carrier",
        "pattern": "tf12",
        "plates": "tf12-c5",
        "layer": "plate_carrier",
        "durability": 2000,
        "basePrice": 3500,
        "dcMod": -3,
        "protection": {
            "torso": [50,85,40],
            "stomach": [30,50,30],
        }
    }

    def __init__(self, wearable):
        self.id = wearable['id']
        self.name = wearable['name']
        self.durability = wearable['durability']
        self.basePrice = wearable['basePrice']
        self.protection = wearable['protection']
        self.layer = wearable['layer']