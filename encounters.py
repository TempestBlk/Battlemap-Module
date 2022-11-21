import random
from errors import PlayerDied
from dice import Dice
from interface import Interface
from items import Weapon
from lifeforms import Lifeform, Mindless, Humanoid, PlayerCharacter


class CombatActor():
    """Model for each combatant in encounter"""
    def __init__(self, lifeform:Lifeform, group:list[Lifeform], hostiles:list[Lifeform]) -> None:
        self.lifeform = lifeform
        self.group = group
        self.hostiles = hostiles



class EncounterReporter:
    """Prints encounter events to console"""
    border = "\n\n-----------------------------"

    def __init__(self) -> None:
        self.round_num = 0
        self.turn_num = 0
        self.round_log: str

    
    def __repr__(self) -> str:
        self.round_log += self.border
        return self.round_log


    def nextRound(self) -> None:
        self.round_log = ""
        self.round_num += 1
        self.round_log = self.border + f"\n\n\t[Round {self.round_num}]"


    def actorInfo(self, lifeform:Lifeform) -> None:
        if lifeform.hp > lifeform.max_hp / 2:
           health = "Healthy"
        elif lifeform.hp > lifeform.max_hp / 4:
            health = "Bloodied"
        else:
            health = "Dying"

        if lifeform.equipped['mainHand'] is not None:
            mainHand = f"{lifeform.equipped['mainHand'].name}"
        else:
            mainHand = "None"

        if lifeform.equipped['offHand'] is not None:
            offHand = f"{lifeform.equipped['offhand']}"
        else:
            offHand = "None"
            
        return f"{lifeform.name} | {health}\nMain-Hand: {mainHand} | Off-Hand: {offHand}"


    def nextTurn(self, actor:CombatActor) -> None:
        self.turn_num += 1
        header = f"\n\nTurn {self.turn_num}"
        header += " : " + self.actorInfo(actor.lifeform)
        self.round_log += header


class Encounter():
    """
    A turn based combat encounter.
    """
    
    def __init__(self, pc:PlayerCharacter, enemies:list[Lifeform], allies:list[Lifeform]=None) -> None:
        self.pc = pc
        if allies is None:
            allies = []
        self.allies = allies + [pc]
        self.enemies = enemies

        self.combatants = self.buildCombatants()
        self.turn_order:list[CombatActor]
        self.sortTurnOrder()
        self.reporter = EncounterReporter()

        self.pc_xp = 0
        self.downed:list[Lifeform] = []
        self.inCombat = True


    def buildCombatants(self) -> list[CombatActor]:
        combatants = []
        for lifeform in self.allies:
            combatants.append(CombatActor(lifeform, self.allies, self.enemies))
        for lifeform in self.enemies:
            combatants.append(CombatActor(lifeform, self.enemies, self.allies))
        return combatants

    
    def sortTurnOrder(self) -> None:
        self.turn_order = sorted(self.combatants, key=lambda x: x.lifeform.init, reverse=True)

    
    def removeActor(self, target:Lifeform) -> None:
        for actor in self.combatants:
            if actor.lifeform is target:
                actor.group.remove(target)
                self.combatants.remove(actor)
        self.downed.append(target)


    def doAttack(self, actor:CombatActor, target:Lifeform, attack:dict) -> None:
        toHit = Dice.roll([1,20,attack["toHit"]])
        toHit = toHit//2
        if toHit < target.dodge_class:
            self.reporter.round_log += f"\n--> Missed {target.name} with {attack['name']}"
            return
        
        damage_reduction:int = target.protection['torso'][attack['damageType']] // 5
        protection = damage_reduction // 2

        for item in list(target.equipped['wearable']): # TODO: check for item break
            item.durability -= 1

        if (protection + target.dodge_class) > toHit:
            self.reporter.round_log += f"\n--> {attack} absorbed by {target.name}'s armor"
            return

        damage = Dice.roll(attack['damage']) # TODO: attack.givenby loses durability

        if damage_reduction == 0:
            self.reporter.round_log += f"\n--> Hit {target.name} with {attack['name']} dealing {damage} damage"
            target.hp -= damage
        elif damage == 1:
            self.reporter.round_log += f"\n--> {attack} absorbed by {target.name}'s armor"
            return
        elif damage_reduction >= damage:
            self.reporter.round_log += f"\n--> Hit {target.name} with {attack['name']} dealing 1 ({damage}-{damage_reduction}) damage"
            target.hp -= 1
        else:
            self.reporter.round_log += f"\n--> Hit {target.name} with {attack['name']} dealing {damage} ({damage}-{damage_reduction}) damage"
            target.hp -= (damage - damage_reduction)

        if target.hp <= 0:
            if actor.lifeform is self.pc:
                self.pc_xp += target.xp_val
            self.reporter.round_log += f"\n--> {target.name} has fallen!"
            self.removeActor(target)
            

    
    def doTurn(self, actor:CombatActor) -> None:
        if not actor.hostiles:
            self.reporter.round_log += "\n--> Waits..."
            return
        action_decider = random.randint(1, 5)
        if action_decider == 0:
            self.reporter.round_log += "\n--> Waits..."
            return
        target = random.choice(actor.hostiles)
        attack = random.choice(actor.lifeform.attacks)
        self.doAttack(actor, target, attack)

    
    def encounterEnd(self, isAlive=True):
        print(f"\t--- [Encounter Ended] ---\n")
        
        if isAlive is False:
            print(f"{self.pc.name} has fallen in battle!")
        else:
            self.pc.addXp(self.pc_xp)
            self.pc.gold_flakes += 5
            print(f"{self.pc.name} gained {self.pc_xp} xp.")

        if self.downed:
            print(f"\nCasualties:")
            for lifeform in self.downed:
                print(f"- {lifeform.name}")
        
        Interface.pressEnter()


    def runEncounter(self) -> None:
        Interface.encounterStart()
        while self.inCombat:
            self.reporter.nextRound()
            self.sortTurnOrder() # TODO: sort turnorder each turn, inverse pop?
            turn_order = list(self.turn_order)
            while turn_order:
                actor = turn_order[0]
                if actor.lifeform not in self.downed:
                    self.reporter.nextTurn(actor)
                    self.doTurn(actor)
                turn_order.remove(actor)
            
            Interface.characterInfo(self.pc)
            print(self.reporter)
            Interface.pressEnter()

            if not self.enemies:
                self.encounterEnd()
                self.inCombat = False

            if self.pc not in self.allies:
                self.encounterEnd(False)
                self.inCombat = False
                raise PlayerDied(self.pc)



class EncounterBuilder():
    """Builds an encounter based on"""

    # NOTE: list[list[lifeform, name, main_hand_weapon]]
    LIGHT = [
        [[Mindless, "Mindless-1"]],
        [[Humanoid, "Vagrant-1"]]
    ]
    AVERAGE = [
        [[Humanoid, "Vagrant-1", Weapon.shiv]],
        [[Mindless, "Mindless-1"], [Mindless, "Mindless-2"]]
    ]
    DIFFICULT = [
        [[Humanoid, "Vagrant-1", Weapon.metal_pipe], [Humanoid, "Vagrant-2", Weapon.shiv]],
        [[Mindless, "Mindless-1", Weapon.metal_pipe], [Mindless, "Mindless-1"], [Mindless, "Mindless-1"]]
    ]


    @classmethod
    def build(self, pc:PlayerCharacter, difficulty_level:int=None, allies:list[Lifeform]=[]) -> Encounter:
        if pc.hp < 0:
            print(f"\n{pc.name} is dead...")
            return Interface.pressEnter()

        difficulty_dict = {1: self.LIGHT, 2: self.AVERAGE, 3: self.DIFFICULT}

        if difficulty_level is None:
            Interface.clear()
            userInput = input("\nChoose a difficulty.\n[1] Light\n[2] Average\n[3] Difficult\n\n[Enter] Go Back\n\n")
            if userInput not in difficulty_dict:
                return Interface.pressEnter()
            difficulty = difficulty_dict[userInput]
        else:
            difficulty = difficulty_dict[difficulty_level]

        scenario = random.choice(difficulty)
        enemies = []
        for enemy in scenario:
            enemy_class = enemy[0]
            lifeform:Lifeform = enemy_class(enemy[1])
            if len(enemy) > 2:
                lifeform.equipWeapon(Weapon(enemy[2]))
            enemies.append(lifeform)

        encounter = Encounter(pc, enemies, allies)
        return encounter