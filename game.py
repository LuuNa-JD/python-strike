# game.py
from environment import Environment
from player import Player
from controls import Controls
from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    WindowProperties, LVector3, ClockObject, CollisionTraverser,
    CollisionHandlerPusher, BitMask32, loadPrcFileData
)
loadPrcFileData('', 'notify-level info')


class PythonStrike(ShowBase):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.disableMouse()

        # Gestion des collisions
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        # Masques de collision
        self.FLOOR_MASK = BitMask32.bit(1)

        # Initialisation des modules
        self.environment = Environment(
            self.loader, self.render, self.FLOOR_MASK)
        self.player = Player(
            self.camera, self.render, self.cTrav, self.pusher, self.FLOOR_MASK
        )
        self.controls = Controls(self)

        # Position et orientation initiales de la caméra
        self.camera.setPos(3, 0, 3)
        self.camera.setHpr(180, 0, 0)

        # Tâches
        self.taskMgr.add(self.move_task, "move_task")

    def move_task(self, task):
        key_map = self.controls.key_map
        speed = 7 * ClockObject.getGlobalClock().getDt()
        direction = LVector3(0, 0, 0)

        if key_map["forward"]:
            direction.y += speed
        if key_map["backward"]:
            direction.y -= speed
        if key_map["left"]:
            direction.x -= speed
        if key_map["right"]:
            direction.x += speed

        # Calcul de la nouvelle position
        new_position = self.camera.getPos() + self.camera.getQuat().xform(
            direction)

        # Ajuste la hauteur en fonction du raycast
        self.cTrav.traverse(self.render)
        entries = list(self.player.ray_queue.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(self.render).getZ())

        if entries:
            ground_z = entries[0].getSurfacePoint(self.render).getZ()
            new_position.z = ground_z + 1

        self.camera.setPos(new_position)
        return task.cont


if __name__ == "__main__":
    game = PythonStrike()
    game.run()
