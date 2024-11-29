from panda3d.core import Fog


class Environment:
    def __init__(self, loader, render, FLOOR_MASK):
        # Charger la carte
        self.map = loader.loadModel("assets/maps/training_military/scene.gltf")
        self.map.reparentTo(render)
        self.map.setScale(0.65)
        self.map.setPos(0, 0, 0)

        # Configurer le brouillard et la skybox
        self.setup_fog(render)
        self.setup_skybox(loader, render)

        # Configurer les collisions
        geom_nodes = self.map.findAllMatches("**/+GeomNode")
        for node in geom_nodes:
            node.node().setIntoCollideMask(FLOOR_MASK)

    def setup_fog(self, render):
        """Configurer le brouillard pour l'ambiance nocturne."""
        fog = Fog("NightFog")
        fog.setColor(0.02, 0.02, 0.05)
        fog.setExpDensity(0.15)  # Densité exponentielle
        fog.setLinearRange(30, 500)  # Plage linéaire pour le brouillard
        self.map.setFog(fog)

    def setup_skybox(self, loader, render):
        """Charger et configurer la skybox."""
        # Charger la skybox
        skybox = loader.loadModel("assets/skybox/skybox.gltf")
        skybox.reparent_to(render)
        skybox.setScale(500)  # Taille de la skybox
        skybox.setTwoSided(True)  # Visible de l'intérieur
        skybox.setDepthWrite(False)  # Ne pas affecter la profondeur
        skybox.setBin("background", 0)  # Toujours en arrière-plan
        skybox.setLightOff()  # Pas de lumière sur la skybox
        skybox.clearFog()

        return skybox
