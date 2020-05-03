import toga

def on_press(widget):
    print("Holis")

def new_button():
    button = toga.Button("Hello World", on_press=on_press)
    button.style.padding = 20
    button.style.font_size = 14
    button.style.width = 200

    return button

def build(app):
    box = toga.Box()
    button1 = new_button()
    box.add(button1)
    return box

def main():
    app = toga.App("Hello World", "page", startup=build)
    return app

if __name__ == "__main__":
    app = main()
    app.main_loop()
