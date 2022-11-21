from interface import Interface
from items import Weapon, Wearable
from lifeforms import PlayerCharacter


class Inventory():


    def open(pc:PlayerCharacter):
        inInventory = True
        while inInventory:
            Interface.clear()
            print("\t--- [Inventory] ---\n\n")
            Interface.characterInfo(pc, stats=False)
            if pc.inventory:
                print("\n[E] Switch to equipped")
                print(f"\nInventory:")
                item_num = 0
                item_dict = {}
                for item in list(pc.inventory):
                    item_num += 1
                    item_dict[f"{item_num}"] = item
                    print(f"[{item_num}] {item.name} ({item.durability})")
                userInput = input("\n[Enter] Go Back\n\n")
                if userInput in item_dict:
                    selected_item = item_dict[userInput]
                    userInput = input("\n[1] Equip\n[2] Drop\n\n[Enter] Go Back\n\n")
                    if userInput == "1":
                        if type(selected_item) is Weapon:
                            pc.equipWeapon(selected_item)
                        elif type(selected_item) is Wearable:
                            pc.equipWearable(selected_item)
                    elif userInput == "2":
                        pc.inventory.remove(selected_item)
    
                elif userInput.lower() == "e":
                    inInventory = Inventory.equipped(pc, inInventory)
                
                else:
                    inInventory = False

            else:
                print("\nInventory: None")
                inInventory = False
                Interface.pressEnter()
    

    def equipped(pc:PlayerCharacter, inInventory):
        inEquipped = True
        while inEquipped:
            Interface.clear()
            print("\t--- [Equipped] ---\n\n")
            item_num = 0
            item_dict = {}
            if pc.equipped['mainHand'] is not None:
                item = pc.equipped['mainHand']
                item_num += 1
                print(f"Main-Hand: [{item_num}] {item.name} ({item.durability})", end=" ")
                item_dict[f"{item_num}"] = [item, 'mainHand']
            else:
                print(f"Main-Hand: None", end=" ")

            if pc.equipped['offHand']:
                item = pc.equipped['offHand']
                item_num += 1
                print(f"| Off-Hand: [{item_num}] {item.name} ({item.durability})")
                item_dict[f"{item_num}"] = [item, 'offhand']
            else:
                print(f"| Off-Hand: None")

            print("Wearing: ", end="")
            if pc.equipped['wearable']:
                print("")
                for item in pc.equipped['wearable']:
                    item_num += 1
                    print(f"[{item_num}] {item.name} ({item.durability})")
                    item_dict[f"{item_num}"] = [item, 'wearable']
            else:
                print("None")
            
            print("\n[E] Switch to inventory")

            userInput = input("\n[Enter] Go Back\n\n")
            if userInput in item_dict:
                selected_item = item_dict[userInput][0]
                equip_type = item_dict[userInput][1]
                userInput = input("\n[1] Unequip\n\n[Enter] Go Back\n\n")
                if userInput == "1":
                    if equip_type == "mainHand":
                        pc.unequipWeapon(selected_item)
                    elif equip_type == "offHand":
                        pass
                    elif equip_type == "wearable":
                        pc.unequipWearable(selected_item)
            elif userInput.lower() == "e":
                inEquipped = False
                return inInventory
            else:
                inEquipped = False
                inInventory = False
                return inInventory