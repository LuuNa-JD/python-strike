from direct.showbase.DirectObject import DirectObject


class ModelCalibrator(DirectObject):
    def __init__(self, model, step=0.1, rotation_step=5):
        self.model = model
        self.step = step
        self.rotation_step = rotation_step

        self.accept("arrow_up", self.move_model, [0, self.step, 0])    # Avancer
        self.accept("arrow_down", self.move_model, [0, -self.step, 0])  # Reculer
        self.accept("arrow_left", self.move_model, [-self.step, 0, 0])  # Gauche
        self.accept("arrow_right", self.move_model, [self.step, 0, 0])  # Droite
        self.accept("q", self.move_model, [0, 0, self.step])  # Monter
        self.accept("e", self.move_model, [0, 0, -self.step])  # Descendre
        self.accept("a", self.rotate_model, [-self.rotation_step, 0, 0])  # Tourner à gauche
        self.accept("d", self.rotate_model, [self.rotation_step, 0, 0])   # Tourner à droite

    def move_model(self, dx, dy, dz):
        self.model.setPos(self.model.getX() + dx, self.model.getY() + dy, self.model.getZ() + dz)
        print(f"Nouvelle position : {self.model.getPos()}")

    def rotate_model(self, h, p, r):
        self.model.setHpr(self.model.getH() + h, self.model.getP() + p, self.model.getR() + r)
        print(f"Nouvelle orientation : {self.model.getHpr()}")
