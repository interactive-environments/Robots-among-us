from components.wifi_setup import WiFi
from components.mqtt_setup import MQTTBroker
from timer import Timer
import random
import time

# All messages in this list will be sent as part of the offline simulation
offline_messages = ["350", "370"]
active_or_standby = 1

offline_timer = Timer()
offline_timer.set_duration(5)

class EcoSystem:
    def __init__(self, ecosystem, creature, connect_to_ecosystem):
        self.connect_to_ecosystem = connect_to_ecosystem
        self.creature = creature
        self.wifi_connected = False
        self.mqtt_connected = False

        if self.connect_to_ecosystem:
            try:
                print("Initializing WiFi...")
                self.wifi = WiFi()
                self.wifi_connected = True
                
                print("Initializing MQTT...")
                self.mqtt = MQTTBroker(self.wifi, ecosystem, self.creature)
                self.mqtt_connected = True
            except Exception as e:
                print(f"Failed to connect to ecosystem: {e}")
                print("Falling back to offline mode")
                self.connect_to_ecosystem = False

    # Sends a message in the ecosystem
    def send_message(self, message):
        print("sending: " + message)
        if self.connect_to_ecosystem and self.mqtt_connected:
            try:
                self.mqtt.send(self.mqtt.client_id + "$$$" + message)
            except Exception as e:
                print(f"Failed to send message: {e}")

    # Checks if there is a message from the robot network
    def check_for_messages(self):
        global offline_messages, offline_timer, active_or_standby
        if self.connect_to_ecosystem and self.mqtt_connected:
            try:
                self.mqtt.loop()
            except Exception as e:
                print(f"MQTT communication error: {e}")
                # Try to reconnect
                try:
                    if hasattr(self, 'wifi') and hasattr(self, 'mqtt'):
                        self.wifi.reset()
                        time.sleep(1)
                        self.mqtt.mqtt_client.reconnect()
                except Exception as reconnect_error:
                    print(f"Failed to reconnect: {reconnect_error}")
        else:
            # Simulate robot network messages in offline mode
            if offline_timer.expired():
                offline_timer.set_duration(60)
                offline_timer.start()
                self.creature.message("reefcontrol/timeofday", offline_messages[active_or_standby])
                if active_or_standby == 0:
                    active_or_standby = 1
                else:
                    active_or_standby = 0