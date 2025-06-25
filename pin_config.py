# pin_config.py
# This file defines the pin mappings for the Raspberry Pi Pico 2W
# If you need to change the pin assignments, you can do it here instead of modifying each component file

import board

# Pin definitions for inputs
BUTTON_PIN = board.GP27      # Button input pin
SLIDER_PIN = board.GP28     # Slider input pin
TOF_PIN_SCL = board.GP9     # ToF sensor SCL pin (I2C)
TOF_PIN_SDA = board.GP8     # ToF sensor SDA pin (I2C)


# Pin definition for outputs
SERVO_PIN = board.GP16       # Servo motor control pin
VIBRATION_PIN = board.GP20   # Vibration motor control pin
NEOPIXEL_PIN = board.GP1    # NeoPixel LED control pin
BUZZER_PIN = board.GP7      # Buzzer control pin
EMAGNET_PIN = board.GP18    # Electromagnet control pin

