from direct.gui.DirectGui import DirectButton, OnscreenImage
from panda3d.core import TransparencyAttrib
from direct.showbase.Loader import Loader


class MenuInterface:
    def __init__(self, base):
        self.base = base
        self.loader = Loader(base)
        self.main_menu_music = self.loader.loadMusic(
            "assets/sounds/main_menu.wav"
        )
        self.main_menu_music.setLoop(True)
        self.main_menu_music.play()

        # Image de fond pour le menu
        self.background = OnscreenImage(
            image="assets/images/menu.jpg",
            pos=(0, 0, 0),
            scale=(1.777, 1, 1)
        )
        self.background.setTransparency(TransparencyAttrib.MAlpha)

        # Bouton Jouer
        self.play_button = DirectButton(
            text="Jouer",
            scale=0.1,
            pos=(0, 0, 0.2),
            command=self.start_game
        )

        # Bouton Quitter
        self.quit_button = DirectButton(
            text="Quitter",
            scale=0.1,
            pos=(0, 0, -0.2),
            command=self.quit_game
        )

    def start_game(self):
        """
        Transition pour lancer le jeu.
        """
        self.base.start_game()

    def quit_game(self):
        """
        Quitte l'application.
        """
        self.base.userExit()

    def cleanup(self):
        """
        Nettoie les éléments de l'interface utilisateur.
        """
        self.play_button.destroy()
        self.quit_button.destroy()
        self.background.destroy()
        self.main_menu_music.stop()
