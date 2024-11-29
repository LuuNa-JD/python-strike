from panda3d.core import (
    CollisionNode,
    CollisionSphere,
    CollisionHandlerPusher,
    BitMask32
)
import random


class Monster:
    def __init__(self, loader, render, model_path, position, FLOOR_MASK):
        # Charger le modèle du monstre
        self.model = loader.loadModel(model_path)
        self.model.reparentTo(render)
        self.model.setScale(0.85)  # Ajuster l'échelle si nécessaire
        self.model.setPos(*position)  # Position initiale (tuple x, y, z)

        # Ajouter une collision pour le monstre
        self.collision_node = CollisionNode('monster_collision')
        self.collision_node.addSolid(CollisionSphere(0, 0, 0, 1))  # Rayon 1
        self.collision_node.setFromCollideMask(FLOOR_MASK)
        self.collision_node.setIntoCollideMask(BitMask32.bit(2))
        self.collision = self.model.attachNewNode(self.collision_node)

        # Gestion des collisions
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.collision, self.model)

        # Comportement par défaut
        self.state = "idle"  # idle, patrolling, chasing
        self.speed = 2  # Vitesse de déplacement

    def patrol(self):
        """Logique pour le déplacement aléatoire."""
        if self.state == "patrolling":
            x = random.uniform(-1, 1) * self.speed
            y = random.uniform(-1, 1) * self.speed
            new_x = self.model.getX() + x
            new_y = self.model.getY() + y
            new_z = self.model.getZ()
            self.model.setPos(new_x, new_y, new_z)

    def chase(self, player_position):
        """Logique pour suivre le joueur."""
        if self.state == "chasing":
            dx = player_position[0] - self.model.getX()
            dy = player_position[1] - self.model.getY()
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                self.model.setX(self.model.getX() + dx / distance * self.speed)
                self.model.setY(self.model.getY() + dy / distance * self.speed)
