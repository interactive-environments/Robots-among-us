# slider.py
import time
from analogio import AnalogIn
from analogio import AnalogOut
import pwmio
from pin_config import SLIDER_PIN

class Slider():
    def __init__(self, port=SLIDER_PIN):
            self.slider = AnalogIn(port)

    def sense(self):
        #print(self.slider.value)
        return (self.slider.value >> 6)
