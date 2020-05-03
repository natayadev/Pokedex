import toga
from const import *

class PokeDex(toga.App):
    def __init__(self, title, id):
        toga.App.__init__(self, title, id)
        self.title = title
        self.size=(WIDTH, HEIGHT)

        self.create_elements(self)

    def startup(self):
        self.main_window = toga.MainWindow("main", title=self.title,size=(400,500))
        box=toga.Box()

        split =  toga.SplitContainer()
        split.content = [self.table, box]


        self.main_window.content = split
        self.main_window.show()

    def create_elements(self):
        self.create_table()

    def create_table(self):
        self.table = toga.Table(["encabezado 1", "encabezado 2"])

#callbacks
if __name__ == "__main__":
    pokedex = PokeDex("PokeDex", "page")
    pokedex.main_loop()
