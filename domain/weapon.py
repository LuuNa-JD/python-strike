from panda3d.core import NodePath, Point3, BoundingSphere, DepthTestAttrib
from direct.actor.Actor import Actor
import random


class Weapon:
    def __init__(self, render, loader, camera: NodePath, model_path: str,
                 frame_ranges: dict = None):
        """
        Initialise une arme générique.
        """
        self.camera = camera
        self.model = None
        self.frame_ranges = frame_ranges or {}

        try:
            print(f"Tentative de chargement du modèle : {model_path}")
            # Chargement du modèle avec animations intégrées
            self.model = Actor(model_path)
            print(f"Modèle chargé avec succès : {model_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle {model_path} : {e}")
            return
        # Reparentement à la caméra du joueur
        self.model.reparentTo(camera)
        self.model.setScale(1)
        self.model.setPos(-0.09, -0.2, -1.6)
        self.model.setHpr(175, 0, 0)

        # Configuration graphique
        self.model.setAttrib(DepthTestAttrib.make(DepthTestAttrib.MLessEqual))
        self.model.setDepthWrite(True)

        # Étendre les bounds pour éviter les disparitions
        bounds = BoundingSphere(Point3(0, 0, 0), 5)
        self.model.node().setBounds(bounds)
        self.model.node().setFinal(True)

        # Appliquer les lumières
        for light in render.find_all_matches("**/+Light"):
            self.model.setLight(light)

        print("Arme initialisée avec succès.")

    def play_animation(self, action: str, loop: bool = True):
        """
        Joue une animation définie par une plage de frames.
        """
        if not self.frame_ranges:
            print("Aucune plage de frames définie pour les animations.")
            return

        if action == "attack":
            idle_variants = [
                key for key in self.frame_ranges.keys()
                if key.startswith("attack")
            ]
            if idle_variants:
                action = random.choice(idle_variants)

        if action not in self.frame_ranges:
            print(f"Aucune plage de frames définie pour l'action '{action}'.")
            return

        from_frame, to_frame = self.frame_ranges[action]

        try:
            if loop:
                self.model.loop("all_anim", fromFrame=from_frame,
                                toFrame=to_frame)
            else:
                self.model.play("all_anim", fromFrame=from_frame,
                                toFrame=to_frame)
            print(f"Animation '{action}' en cours ({from_frame} à "
                  f"{to_frame}).")
        except Exception as e:
            print(f"Erreur lors de la lecture de l'animation : {e}")

    def remove(self):
        """
        Supprime l'arme de la scène.
        """
        self.model.detachNode()
