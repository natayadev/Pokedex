import toga
import requests
import threading

from const import *

from toga.style.pack import *

class PokeDex(toga.App):
    def __init__(self, title, id):
        toga.App.__init__(self, title, id)

        self.title = title
        self.size = (WIDTH, HEIGHT)

        self.heading = ["Name"]
        self.data = list()

        self.offset = 0

        self.response_name = ""
        self.response_description = ""
        self.response_sprite = ""

        self.create_elements()
        self.load_async_data()
        self.validate_previous_command()

    def handler_command(self, widget):
        widget.enabled = False
        self.load_async_data()

        widget.enabled = True
        self.validate_previous_command()

    def startup(self):
        self.main_window = toga.MainWindow("main", title=self.title,size=(400,500))
        information_area=toga.Box(
            children=[self.image_view, self.pokemon_name, self.pokemon_description],
            style=Pack(
                direction=COLUMN,
                alignment=CENTER
            )
        )

        split =  toga.SplitContainer()
        split.content = [self.table, information_area]


        self.main_window.content = split
        self.main_window.toolbar.add(self.previous_command, self.next_command)
        self.main_window.show()

    def create_elements(self):
        self.create_table()
        self.create_toolbar()
        self.create_image(PIDGEY_ICON)
        self.create_label()

    def create_label(self):
        style=Pack(text_align=CENTER)

        self.pokemon_name = toga.Label(TITLE, style=style)
        self.pokemon_description = toga.Label("Description", style=style)
        self.pokemon_name.style.font_size = 20
        self.pokemon_name.style.padding_bottom = 10

    def create_toolbar(self):
        self.create_next_command()
        self.create_previous_command()

    def create_next_command(self):
        self.next_command = toga.Command(self.next, label="Next", icon=BULBASAUR_ICON)

    def create_previous_command(self):
        self.previous_command = toga.Command(self.previous, label="Previous", icon=METAPOD_ICON)

    def create_table(self):
        self.table = toga.Table(self.heading, data=self.data, on_select=self.select_element)

    def create_image(self, path, width=200, height=200):
        self.default_image = toga.Image(path)

        style = Pack(width=width,height=height)

        self.image_view = toga.ImageView(self.default_image, style=style)

    def load_async_data(self):
        self.data.clear()
        self.table.data = self.data

        self.image_view.image = None
        self.pokemon_name.text = "Loanding..."
        self.pokemon_description.text = ""

        thread=threading.Thread(target=self.load_data)
        thread.start()
        thread.join()

        self.table.data = self.data
        self.image_view.image = self.default_image
        self.pokemon_name.text = TITLE

    def load_async_pokemon(self, pokemon):
        thread=threading.Thread(target=self.load_pokemon, args=[pokemon])
        thread.start()
        thread.join()

        self.image_view.image = toga.Image(self.response_sprite)
        self.pokemon_name.text = self.response_name
        self.pokemon_description.text = self.response_description

    def load_pokemon(self, pokemon):
        path = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon)
        response = requests.get(path)
        if response:
            result = response.json()

            self.response_name = result["forms"][0]["name"]
            abilities = list()
            for ability in result["abilities"]:
                name_ability = ability["ability"]["name"]
                abilities.append(name_ability)

            self.response_sprite = result["sprites"]["front_default"]
            self.response_description = " ".join(abilities)

            print(name)
            print(abilities)
            print(sprite)

    def load_data(self):
        path = "https://pokeapi.co/api/v2/pokemon-form?offset={}&limit=20".format(self.offset)

        response = request.get(path)
        if response:
            result = responde.json()
            print(row.name)

            for pokemon in result["results"]:
                name=pokemon["name"]
                self.data.append(name)

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
            self.load_async_pokemon(row.name)

if __name__ == "__main__":
    pokedex = PokeDex("PokeDex", "page")
    pokedex.main_loop()
