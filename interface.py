import os


class Interface:
    def clear():
        clear = lambda: os.system('cls')
        clear()


    def pressEnter():
        input("\n\nPress Enter to continue... ")
        Interface.clear()