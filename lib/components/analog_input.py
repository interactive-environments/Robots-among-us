import board
import analogio
from pin_config import SLIDER_PIN


class AnalogInput():
    def __init__(self, port=SLIDER_PIN):
        self.input = analogio.AnalogIn(port)

    def sense(self, threshold):
        return self.input.value > threshold

    def sense_value(self):
        return self.input.value / 65536 * 100
