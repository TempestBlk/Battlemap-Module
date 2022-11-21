import random


class Dice():
    def roll(roll) -> int:
        amount = roll[0]
        die = roll[1]
        if len(roll) < 3:
            mod = 0
        else:
            mod = roll[2]

        total = 0
        for _ in range(0, amount):
            roll = random.randint(1, die)
            total += roll

        total += mod
        return total