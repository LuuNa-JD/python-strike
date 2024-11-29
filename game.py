from domain.environment import Environment
from domain.player import Player
from interfaces.controls_adapter import Controls
import simplepbr
from panda3d.core import (
    WindowProperties, CollisionTraverser,
    CollisionHandlerPusher, BitMask32, loadPrcFileData
)
from domain.monster import Monster
from use_cases.move_player import move_player

loadPrcFileData('', 'win-size 1920 1080')
loadPrcFileData('', 'fullscreen 1')
loadPrcFileData('', 'textures-power-2 none')
loadPrcFileData('', 'framebuffer-multisample 0')
loadPrcFileData('', 'multisamples 0')
loadPrcFileData('', 'interpolate-frames 1')
loadPrcFileData('', 'sync-video false')


class PythonStrike:
    def __init__(self, base):
        self.base = base

        simplepbr.init(
            render_node=self.base.render,
            enable_shadows=False,
            max_lights=20,
            msaa_samples=8,
            shadow_bias=0.05,
            enable_fog=True,
            use_occlusion_maps=True,
            use_emission_maps=True,
            use_normal_maps=True
        )

        # Configuration de la fenêtre
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setFullscreen(True)
        self.base.win.requestProperties(props)
        self.base.disableMouse()

        # Gestion des collisions
        self.base.cTrav = CollisionTraverser()
        self.base.pusher = CollisionHandlerPusher()
        self.FLOOR_MASK = BitMask32.bit(1)

        # Initialisation des modules
        self.environment = Environment(
            self.base.loader, self.base.render, self.FLOOR_MASK)
        self.player = Player(
            self.base.camera, self.base.render, self.base.cTrav,
            self.base.pusher, self.FLOOR_MASK,
            self.base.loader
        )
        self.controls = Controls(self.base)
        self.monster = Monster(
            self.base.loader,
            self.base.render,
            "assets/monsters/fat/fat.gltf",
            position=(5, 5, 0),
            FLOOR_MASK=self.FLOOR_MASK
        )

        # Position caméra
        lens = self.base.cam.node().getLens()
        lens.setNear(0.05)
        lens.setFov(90)
        self.base.camera.setPos(0, -1, 1.5)
        self.base.camera.lookAt(0, 0, 1.5)

        # Tâches
        self.base.taskMgr.add(self.move_task, "move_task")
        self.base.taskMgr.add(
            self.monster_behavior_task, "monster_behavior_task"
        )

    def move_task(self, task):
        """
        Gestion des déplacements du joueur.
        """
        move_player(
            self.base.camera, self.controls, self.base.cTrav,
            self.base.render, self.player
        )
        self.player.update_state(self.controls.key_map)
        return task.cont

    def monster_behavior_task(self, task):
        player_position = (
            self.base.camera.getX(),
            self.base.camera.getY(),
            self.base.camera.getZ()
        )
        if self.monster.state == "patrolling":
            self.monster.patrol()
        elif self.monster.state == "chasing":
            self.monster.chase(player_position)
        return task.cont
