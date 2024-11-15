from panda3d.core import BitMask32, NodePath


class Environment:
    def __init__(self, loader, render: NodePath, FLOOR_MASK: BitMask32):
        # Chargement de la carte
        self.map = loader.loadModel("assets/maps/scene.bam")
        self.map.reparentTo(render)
        self.map.setScale(1)
        self.map.setPos(0, 0, 0)

        # Ajouter une surface de collision
        geom_nodes = self.map.findAllMatches("**/+GeomNode")
        for node in geom_nodes:
            node.node().setIntoCollideMask(FLOOR_MASK)
