import toga
import requests
import threading

from const import *

class PokeDex(toga.App):
    def __init__(self, title, id):
        toga.App.__init__(self, title, id)

        self.title = title
        self.size = (WIDTH, HEIGHT)

        self.heading = ["Name"]
        self.data = list()

        self.offset = 0

        self.create_elements(self)

    def handler_command(self, widget):
        widget.enabled = False
        self.load_async_data()

        widget.enabled = True
        self.validate_previous_command()

    def startup(self):
        self.main_window = toga.MainWindow("main", title=self.title,size=(400,500))
        box=toga.Box()

        split =  toga.SplitContainer()
        split.content = [self.table, box]


        self.main_window.content = split
        self.main_window.toolbar.add(self.previous_command, self.next_command)
        self.main_window.show()

    def create_elements(self):
        self.create_table()
        self.create_toolbar()

    def create_toolbar(self):
        self.create_next_command()
        self.create_previous_command()

    def create_next_command(self):
        self.next_command = toga.Command(self.next, label="Next", icon=BULBASAUR_ICON)

    def create_previous_command(self):
        self.previous_command = toga.Command(self.previous, label="Previous", icon=METAPOD_ICON)

    def create_table(self):
        self.table = toga.Table(self.heading, data=self.data, on_select=self.select_element)

    def load_async_data(self):
        thread=threading.Thread(target=self.load_data)
        thread.start()

    def load_data(self):
        self.data.clear()
        path="https://pokeapi.co/api/v2/pokemon-form?offset={}&limit=20".format(self.offset)

        response = request.get(path)
        if response:
            result = responde.json()

            for pokemon in result["results"]:
                name=pokemon["name"]
                self.data.append(name)

        self.table.data = self.data

#callbacks
    def next(self, widget):
        self.offset += 1
        self.handler_command(widget)

    def previous(self, widget):
        self.offset -= 1
        self.handler_command(widget)

    def validate_previous_command(self):
        self.previous_command.enabled = not self.offset == 0

    def select_elements(self, widget, row):
        if row:
            print(row.name)

if __name__ == "__main__":
    pokedex = PokeDex("PokeDex", "page")
    pokedex.main_loop()
