from abc import ABCMeta
from interface import Interface


class Npc(metaclass=ABCMeta):
    pass



class Doctor(Npc):
    pass



class Merchant(Npc):
    pass



class SeniorResearcherLydia(Doctor):
    title_card = "\t--- [Senior Researcher Lydia] ---\n\n"

    @staticmethod
    def startDialogue(pc):
        Interface.clear()
        print(SeniorResearcherLydia.title_card)

        print("Not too bad, let me patch you up.")
        Interface.pressEnter()



class QuartermasterMathias(Merchant):
    title_card = "\t--- [Quartermaster Mathias] ---\n\n"
    greeting = "Welcome. How can I help?\n"

    @staticmethod
    def startDialogue(pc):
        inDialogue = True
        while inDialogue:
            Interface.clear()
            print(QuartermasterMathias.title_card)
            print(QuartermasterMathias.greeting)
            
            userInput = input("\n[1] Weapons\n[2] Wearables\n[3] Sell\n\n[Enter] Go Back\n\n")
            if userInput == "":
                inDialogue = False