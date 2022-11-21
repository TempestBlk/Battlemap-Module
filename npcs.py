from abc import ABCMeta
from interface import Interface
from items import Item, Weapon, Wearable
from lifeforms import PlayerCharacter


class Npc(metaclass=ABCMeta):
    pass



class Doctor(Npc):
    pass



class Merchant(Npc):
    title_card:str
    greeting:str
    not_enough:str

    sell_mod:float
    buy_mod:float
    for_sale:dict

    def BuyMenu(self, pc:PlayerCharacter, comment, items, item_type):
        inBuyMenu = True
        while inBuyMenu:
            Interface.clear()
            print(self.title_card)
            print(comment)
            item_num = 0
            item_dict = {}
            for item in items:
                item_num += 1
                final_price = round(item['basePrice'] * self.buy_mod)
                item_dict[f"{item_num}"] = [item, final_price]
                print(f"[{item_num}] {item['name']} - {final_price} flakes")
            userInput = input("\n[Enter] Go back\n\n")
            if userInput in item_dict:
                item = item_dict[userInput][0]
                final_price = item_dict[userInput][1]
                if pc.gold_flakes >= final_price:
                    userInput = input(f"\n[1] Buy for {final_price} flakes\n[Enter] Go back\n\n")
                    if userInput == "1":
                        pc.gold_flakes -= final_price
                        built_item = Item.build(Item, item_type, item)
                        pc.inventory.append(built_item)
                else:
                    print(self.not_enough)
                    Interface.pressEnter()
            else:
                inBuyMenu = False

    
    def SellMenu(self, pc:PlayerCharacter, comment:str):
        Interface.clear()
        print(self.title_card)
        print(comment)
        print(f"\nInventory:")
        item_num = 0
        item_dict = {}   
        for item in list(pc.inventory):
            item_num += 1
            final_price = round(item.basePrice * self.sell_mod)
            item_dict[f"{item_num}"] = [item, final_price]
            print(f"[{item_num}] {item.name} - {final_price} flakes")
        userInput = input("\n[Enter] Go Back\n\n")
        if userInput in item_dict:
            item_num = userInput
            selected_item = item_dict[userInput][0]
            userInput = input("\n[1] Sell\n\n[Enter] Go Back\n\n")
            if userInput == "1":
                pc.gold_flakes += item_dict[item_num][1]
                pc.inventory.remove(selected_item)




class SeniorResearcherLydia(Doctor):
    from lifeforms import PlayerCharacter
    
    title_card = "\t--- [Senior Researcher Lydia] ---\n\n"

    @staticmethod
    def startDialogue(pc:PlayerCharacter):
        Interface.clear()
        print(SeniorResearcherLydia.title_card)

        if pc.hp == pc.max_hp:
            print("You're healthy enough. Stop wasting my time!")
        elif pc.hp > pc.max_hp * 0.5:
            print("Not too bad, let me patch you up.")
        elif pc.hp > pc.max_hp * 0.25:
            print("You're not looking too hot...\nHave a seat and bite down on this.")
        elif pc.hp > 0:
            print("Set them down here! We'll start surgery immediately.")
        else:
            print(f"{pc.name} is dead...\nGet their body in the Anubis Chamber.")
        pc.hp = pc.max_hp

        Interface.pressEnter()



class QuartermasterMathias(Merchant):
    title_card = "\t--- [Quartermaster Mathias] ---\n\n"
    greeting = "Welcome. How can I help?\n"
    
    not_enough = "\nYou'll need more flakes for this..."
    sell_mod = 0.25
    buy_mod = 1.20
    for_sale = {
        "weapons": [Weapon.shiv, Weapon.metal_pipe, Weapon.bondprint_sabre],
        "wearables": [Wearable.researcher_garb, Wearable.junior_researcher_coat, Wearable.modified_researcher_coat, Wearable.gensec_patrol_vest]
        }
    sell_to = True

    @classmethod
    def startDialogue(self, pc):
        inDialogue = True
        while inDialogue:
            Interface.clear()
            print(self.title_card)
            print(self.greeting)
            
            userInput = input("\n[1] Weapons\n[2] Wearables\n[3] Sell\n\n[Enter] Go Back\n\n")
            if userInput == "1":
                comment = "Tired of beating Mindless with your fists?\nHave a look at these.\n"
                items = self.for_sale['weapons']
                self.BuyMenu(pc, comment, items, 'weapon')
            elif userInput == "2":
                comment = "Most've our armor's in-use...\nThis is all I've got left.\n"
                items = self.for_sale['wearables']
                self.BuyMenu(pc, comment, items, 'wearable')
            elif userInput == "3":
                comment = "What've you got?"
                Merchant.SellMenu(self, pc, comment)
            else:
                inDialogue = False