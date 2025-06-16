from creature import Creature
from ecosystem import EcoSystem
from timer import Timer
import time

try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add or change them there!")
    raise

# Instantiate the creature - telling a science centre story
creature = Creature()

# This version uses offline mode (connect_to_ecosystem=False)
# In this mode, it will simulate the ecosystem without requiring WiFi
# Useful for testing hardware without a network connection
ecosystem = EcoSystem(ecosystem="reef", creature=creature, connect_to_ecosystem=False)

# add the ecosystem to the creature
creature.ecosystem = ecosystem

while True:
    # This will check for new messages.
    # In offline mode, it will simulate messages
    ecosystem.check_for_messages()

    # This will trigger the default behaviour that will play.
    # regardless if there is a message or not.
    creature.loop()
    time.sleep(0.01)