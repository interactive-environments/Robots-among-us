from components.button import Button
from components.buzzer import Buzzer
from components.neopixel_led import NeopixelLED
from components.vibration_motor import VibrationMotor
from components.servo_motor import Servo
from components.slider import Slider
from components.tof import Tof
from components.electro_magnet import ElectroMagnet
from timer import Timer
import time
from varspeed import Vspeed
from behaviours import Behaviours
import random
import math


# Select your inputs and outputs by uncommenting them here
##########################################################

button = Button()
buzzer = Buzzer()
motor = VibrationMotor()
led = NeopixelLED(1)
servo = Servo()
behaviours = Behaviours()
tof = Tof()
electromagnet = ElectroMagnet()
slider = Slider()

###########################################################

increase = True
led_power = 255
color = (1, 0, 0, 0)

MIN = 0
MAX = 2 ** 16
vs1 = Vspeed(init_position=0, result="int", debug=False)
vs1.set_bounds(lower_bound=MIN, upper_bound=MAX)
vs2 = Vspeed(init_position=0, result="int", debug=False)
vs2.set_bounds(lower_bound=MIN, upper_bound=MAX)


class Creature:
    state_active_idle = 0
    state_active_detected = 1
    state_standby_idle = 2
    state_standby_detected = 3
    state_task_mode = 4

    task_duration = 30
    detection_duration = 5
    detection_timer = Timer(30)
    time_of_day = 0
    energy = 0

    previous_state = state_task_mode
    current_state = state_active_idle

    def __init__(self):
        self.ecosystem = None

    def message(self, topic, msg):
        global color
        # print("recieved: Topic:" + str(topic) + " Message:" + str(msg))

        # If we receive a new time of day
        if topic == "reefcontrol/timeofday":
            # Update the time of day (active hours vs standby hours)
            self.time_of_day = int(msg)
            #print("Updated time of day " + str(self.time_of_day))
        if topic == "reefcontrol/energy":
            # Update the robot's energy level
            self.energy = int(msg)

###################################################
    # uncomment the Time of Flight or slider code if you want to use it


    def sense(self):
        if button.sense() == True:
            return True

        #distance = 150 #distance in mm
        #if tof.sense(distance) == True:
        #    return True()
        #print(tof.sense_range())

        #if slider.sense() > 100:
        # return True
        #print (slider.sense())


###################################################

    def print_state(self):
        if self.current_state != self.previous_state:
            if self.current_state == 0:
                print("*** state_active_idle (day)")
            elif self.current_state == 1:
                print("*** state_active_detected (day motion)")
            elif self.current_state == 2:
                print("*** state_standby_idle (night)")
            elif self.current_state == 3:
                print("*** state_standby_detected (night motion)")
            elif self.current_state == 4:
                print("*** state_task_mode (beautiful)")
        self.previous_state = self.current_state

    def checkState(self, isRunning):
        #print(self.detection_timer)
        if self.current_state == self.state_active_idle:
            if self.sense():
                self.current_state = self.state_active_detected
                self.detection_timer.set_duration(self.detection_duration)
                self.detection_timer.start()
            elif self.time_of_day < 360 or self.time_of_day > 1080:
                self.current_state = self.state_standby_idle
            elif self.detection_timer.expired():
                self.current_state = self.state_task_mode

        elif self.current_state == self.state_active_detected:
            if self.sense():
                self.detection_timer.start()
            elif self.time_of_day < 360 or self.time_of_day > 1080:
                self.current_state = self.state_standby_detected
            elif self.detection_timer.expired():
                self.current_state = self.state_active_idle
                self.detection_timer.set_duration(self.task_duration)
                self.detection_timer.start()

        elif self.current_state == self.state_standby_idle:
            if self.sense():
                self.current_state = self.state_standby_detected
                self.detection_timer.set_duration(self.detection_duration)
                self.detection_timer.start()
            elif self.time_of_day > 360 and self.time_of_day < 1080:
                self.current_state = self.state_active_idle
                self.detection_timer.set_duration(self.task_duration)
                self.detection_timer.start()

        elif self.current_state == self.state_standby_detected:
            if self.sense():
                self.detection_timer.start()
            elif self.time_of_day > 360 and self.time_of_day < 1080:
                self.current_state = self.state_active_detected
                self.detection_timer.set_duration(self.detection_duration)
                self.detection_timer.start()
            elif self.detection_timer.expired():
                self.current_state = self.state_standby_idle

        elif self.current_state == self.state_task_mode:
            if not isRunning:
                self.current_state = self.state_active_idle
                self.detection_timer.set_duration(self.task_duration)
                self.detection_timer.start()



    def loop(self):
        beh = behaviours.getBehaviour(self.current_state)
        position1, running1, changed1 = vs1.sequence(beh[0], beh[1]) # Here we input the sequence from sequence.py and our most important output is position1. This is the number we should currently be at when following our sequence
        position2, running2, changed2 = vs2.sequence(beh[2], beh[3]) # Same as above but for our second sequence

        self.checkState(running1 or running2)
        self.print_state()

        ###############################################################
        # Robot control outputs                                       #
        # Hardware configuration:                                     #
        # - Button (human detection) on GP16                          #
        # - Servo motor (movement) on GP15                            #
        # - Vibration motor (haptic feedback) on GP14                 #
        # - NeoPixel LED (visual indicators) connected                #
        ###############################################################

        #buzzer.update(50)
        #buzzer.set_frequency(2000)
        #electromagnet.update(position1)
        #led.update_full_color((position1,0,position2//1000,0)) # Robot-themed color (red + blue)
        #motor.update(position1) # Controls the robot's vibration intensity
        servo.update(position2) # Controls the robot's movement mechanism
