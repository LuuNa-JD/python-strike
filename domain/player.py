from panda3d.core import (
    CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerQueue,
    BitMask32, NodePath, CollisionTraverser, CollisionHandlerPusher
)
from domain.weapon import Weapon


class Player:
    def __init__(
        self,
        camera: NodePath,
        render: NodePath,
        cTrav: CollisionTraverser,
        pusher: CollisionHandlerPusher,
        FLOOR_MASK: BitMask32,
        loader
    ):

        self.camera = camera
        self.render = render
        self.loader = loader
        self.weapons = []
        self.current_weapon = 0
        self.current_state = None

        self.add_weapon("assets/weapons/knife/knife.gltf", {
            "idle": (36, 300),
            "move": (301, 332),
            "attack_1": (353, 405),
            "attack_2": (406, 442),
        })
        self.equip_weapon(0)
        # self.equip_weapon(0)
        # Sphère de collision pour le joueur
        player_collider = CollisionNode('player')
        player_collider.addSolid(CollisionSphere(0, 0, 0, 0.5))
        player_collider.setFromCollideMask(FLOOR_MASK)
        player_collider.setIntoCollideMask(BitMask32.allOff())
        self.player_node = camera.attachNewNode(player_collider)
        cTrav.addCollider(self.player_node, pusher)
        pusher.addCollider(self.player_node, camera)

        # Raycast pour détecter le sol
        ray = CollisionRay(0, 0, 10, 0, 0, -1)
        ray_collider = CollisionNode('playerRay')
        ray_collider.addSolid(ray)
        ray_collider.setFromCollideMask(FLOOR_MASK)
        ray_collider.setIntoCollideMask(BitMask32.allOff())
        self.ray_node = camera.attachNewNode(ray_collider)
        self.ray_queue = CollisionHandlerQueue()
        cTrav.addCollider(self.ray_node, self.ray_queue)

    def add_weapon(self, model_path: str, frame_ranges: dict):
        """
        Ajoute une nouvelle arme à l'inventaire.
        """
        weapon = Weapon(
            self.render, self.loader, self.camera, model_path, frame_ranges
        )
        if weapon.model:
            self.weapons.append(weapon)
            print(f"Arme ajoutée : {model_path}")
        else:
            print(f"Échec du chargement de l'arme : {model_path}")

    def equip_weapon(self, index: int):
        """
        Change l'arme équipée.
        """
        if 0 <= index < len(self.weapons):
            if self.current_weapon:
                self.current_weapon.remove()
            self.current_weapon = self.weapons[index]
            print(f"Arme équipée : {self.current_weapon.model}")
        else:
            print("Index d'arme invalide.")

    def update_state(self, key_map):
        """
        Met à jour l'état du joueur et joue l'animation correspondante.
        """
        if key_map["attack"]:  # Clique gauche
            new_state = "attack"
        elif (key_map["forward"] or key_map["backward"] or
              key_map["left"] or key_map["right"]):
            new_state = "move"
        else:
            new_state = "idle"

        # Joue l'animation uniquement si l'état a changé
        if new_state != self.current_state:
            self.current_state = new_state
            if self.current_weapon:
                self.current_weapon.play_animation(self.current_state)
