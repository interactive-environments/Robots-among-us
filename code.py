import mac_and_networks
from creature import Creature
from ecosystem import EcoSystem
from timer import Timer
import time

try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add or change them there!")
    raise

# Instantiate the robot - part of the "Robots Among Us" installation
creature = Creature()

# class initialization only connects to wifi/broker if flag is True
# ecosystem.py has all the wifi and mqtt code, parameters in settings.py
# "ecosystem" is the name of the mqtt topic
# "Creature" is the robot object create above
# "connect_to_ecosystem" indicates if the robot should connect to the robot network.
#   If this is set to "false" it will randomly send messages in order to simulate the robot network
ecosystem = EcoSystem(ecosystem="reef", creature=creature, connect_to_ecosystem=True)

# add the ecosystem to the creature
creature.ecosystem = ecosystem

while True:
    # This will check for new messages.
    # The behaviour for theses messages is in creature.py -> message()
    ecosystem.check_for_messages()

    # This will trigger the default behaviour that will play.
    # regardless if there is a message or not.
    creature.loop()
    time.sleep(0.01)
