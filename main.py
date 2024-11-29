from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase
from interfaces.menu_interface import MenuInterface
from game import PythonStrike


class MainApp(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.show_cursor()
        self.setWindowProperties()

        # Lancer le menu principal
        self.menu = MenuInterface(self)

    def show_cursor(self):
        """
        Affiche le curseur.
        """
        props = WindowProperties()
        props.setCursorHidden(False)
        self.win.requestProperties(props)

    def hide_cursor(self):
        """
        Cache le curseur.
        """
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)

    def setWindowProperties(self):
        """
        Configure les propriétés de la fenêtre.
        """
        props = WindowProperties()
        props.setFullscreen(True)
        self.win.requestProperties(props)

    def start_game(self):
        """
        Lance la partie en fermant le menu.
        """
        self.menu.cleanup()
        self.menu = None
        self.hide_cursor()
        self.game = PythonStrike(self)


if __name__ == "__main__":
    app = MainApp()
    app.run()
