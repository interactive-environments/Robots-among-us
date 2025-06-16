# vibration motor

import time
import pwmio
import digitalio
from pin_config import VIBRATION_PIN

class VibrationMotor():
    def __init__(self,port=VIBRATION_PIN):
        self.motor = pwmio.PWMOut(port, frequency=300, duty_cycle=0)

    # Takes either true or false
    def update(self, value):
        self.motor.duty_cycle = value