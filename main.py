import toga

def build(app):
    box = toga.Box()
    return box

def main():
    app = toga.App("Hello World", "page", startup=build)
    return app

if __name__ == "__main__":
    app = main()
    app.main_loop()
    
