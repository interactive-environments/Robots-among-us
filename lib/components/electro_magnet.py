# electro_magnet.py

import board
import digitalio
from pin_config import EMAGNET_PIN

class ElectroMagnet():
    def __init__(self, port=EMAGNET_PIN):
        self.magnet = digitalio.DigitalInOut(port)
        self.magnet.direction = digitalio.Direction.OUTPUT

    # Takes either true or false
    def update(self, value):
        print(value)
        if value > 0:
            self.magnet.value = True
        else:
            self.magnet.value = False
