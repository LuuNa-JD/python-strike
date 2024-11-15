from panda3d.core import (
    CollisionNode, CollisionSphere, CollisionRay, CollisionHandlerQueue,
    BitMask32, NodePath, CollisionTraverser, CollisionHandlerPusher
)


class Player:
    def __init__(
        self,
        camera: NodePath,
        render: NodePath,
        cTrav: CollisionTraverser,
        pusher: CollisionHandlerPusher,
        FLOOR_MASK: BitMask32
    ):
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
