class Controls:
    def __init__(self, base):
        self.base = base
        self.camera = base.camera
        self.win = base.win
        self.mouseWatcherNode = base.mouseWatcherNode

        # Gestion des touches
        self.key_map = {
            "forward": 0,
            "backward": 0,
            "left": 0,
            "right": 0,
            "attack": 0
        }
        base.accept("z", self.update_key_map, ["forward", 1])
        base.accept("z-up", self.update_key_map, ["forward", 0])
        base.accept("s", self.update_key_map, ["backward", 1])
        base.accept("s-up", self.update_key_map, ["backward", 0])
        base.accept("q", self.update_key_map, ["left", 1])
        base.accept("q-up", self.update_key_map, ["left", 0])
        base.accept("d", self.update_key_map, ["right", 1])
        base.accept("d-up", self.update_key_map, ["right", 0])

        # Clic gauche pour "attack"
        base.accept("mouse1", self.update_key_map, ["attack", 1])
        base.accept("mouse1-up", self.update_key_map, ["attack", 0])

        base.accept("escape", base.userExit)

        # Sensibilité de la souris
        self.mouse_sensitivity = 0.1
        self.pitch = 0  # Rotation verticale

        # Tâche pour le contrôle de la souris
        base.taskMgr.add(self.mouse_control_task, "mouse_control_task")

        # Centrage de la souris
        self.win_size = (self.win.getXSize(), self.win.getYSize())
        self.win.movePointer(0, self.win_size[0] // 2, self.win_size[1] // 2)

    def update_key_map(self, key, value):
        self.key_map[key] = value

    def mouse_control_task(self, task):
        win_width, win_height = self.win_size
        center_x = win_width // 2
        center_y = win_height // 2

        if self.mouseWatcherNode.hasMouse():
            mouse_x = self.win.getPointer(0).getX() - center_x
            mouse_y = self.win.getPointer(0).getY() - center_y

            new_heading = self.camera.getH() - mouse_x * self.mouse_sensitivity
            self.camera.setH(new_heading)
            self.pitch -= mouse_y * self.mouse_sensitivity
            self.pitch = max(-90, min(90, self.pitch))
            self.camera.setP(self.pitch)

            self.win.movePointer(0, center_x, center_y)

        return task.cont
