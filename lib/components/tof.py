# Tof.py

import time
from pin_config import TOF_PIN_SCL, TOF_PIN_SDA
import busio
import adafruit_vl53l0x

class Tof():
    def __init__(self):
        self.i2c = busio.I2C(TOF_PIN_SCL, TOF_PIN_SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)

    def sense(self, distance):
        return self.vl53.range < distance and self.vl53.range > 20

    def sense_range(self):
        return self.vl53.range
