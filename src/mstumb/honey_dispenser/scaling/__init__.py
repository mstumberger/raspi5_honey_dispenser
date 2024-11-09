class Dispenser:
    speed = 2
    jars_filled = 0
    target_weight = 800
    current_step = 0

    def __init__(self, config, initial_weight=None, speed=0):
        pass

    def check_weight(self):
        return 0

    def fill_jar(self):
        pass

    def tare_scale(self):
        pass

    def calibrate(self):
        pass

    def rotate_stepper(self, steps, direction):
        pass