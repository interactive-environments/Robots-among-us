# mqtt_setup.py
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import time

class MQTTBroker():

    def __init__(self, wifi, topic, creature):
        try:
            from settings import settings
        except ImportError:
            print("WiFi settings are kept in settings.py, please add or change them there!")
            raise
        self.settings = settings
        self.wifi = wifi
        self.default_topic = topic
        self.client_id = self.settings["mqtt_clientid"]

        # Configure MQTT client
        self.mqtt_client = MQTT.MQTT(
            client_id = self.client_id,
            broker=settings["mqtt_broker"],
            username=settings["mqtt_broker_user"],
            password=settings["mqtt_broker_password"],
            socket_pool=self.wifi.pool,
            ssl_context=self.wifi.ssl_context,
            socket_timeout=.11,  # Increased timeout for more reliability
            keep_alive=60  # Keep-alive ping interval
        )

        self.creature = creature

        # Set up callback functions
        self.mqtt_client.on_connect = self.connected
        self.mqtt_client.on_disconnect = self.disconnected
        self.mqtt_client.on_message = self.message

        # Connect with retry mechanism
        print("Connecting to MQTT broker...")
        self._connect_with_retry()

    def _connect_with_retry(self, max_attempts=3):
        """Connect to MQTT broker with retries"""
        attempt = 0
        while attempt < max_attempts:
            try:
                self.mqtt_client.connect()
                print(f"Connected to MQTT broker: {self.settings['mqtt_broker']}")
                return True
            except Exception as e:
                attempt += 1
                print(f"MQTT connection attempt {attempt} failed: {e}")
                if attempt >= max_attempts:
                    print("Failed to connect to MQTT broker after multiple attempts")
                    raise
                time.sleep(2)  # Wait before retrying
        return False

    def message(self, client, topic, message):
        """Handle incoming MQTT messages"""
        try:
            self.creature.message(topic, message)
        except Exception as e:
            print(f"Error processing message from topic {topic}: {e}")

    ### MQTT connection functions ###
    def connected(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        print(f"Connected to MQTT broker! Listening for topic changes on {self.default_topic}")
        # Subscribe to topics
        try:
            client.subscribe("reefcontrol/timeofday")
            client.subscribe("reefcontrol/energy")
        except Exception as e:
            print(f"Error subscribing to topics: {e}")

    def disconnected(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        print("Disconnected from MQTT Broker!")

    def send(self, message):
        """Send a message to the default topic"""
        try:
            self.mqtt_client.publish(self.default_topic, message)
            return True
        except Exception as e:
            print(f"Error publishing message: {e}")
            return False

    def loop(self):
        """Process MQTT messages"""
        try:
            self.mqtt_client.loop(.11)
        except (ValueError, RuntimeError, OSError) as e:
            print(f"Failed to process MQTT messages: {e}")
            # Try to reconnect
            self._reconnect()

    def _reconnect(self, max_attempts=1):
        """Attempt to reconnect to MQTT"""
        attempt = 0
        while attempt < max_attempts:
            try:
                print("Attempting to reconnect to MQTT...")
                # Ask WiFi to reset connection first
                self.wifi.reset()
                time.sleep(1)  # Give WiFi time to stabilize

                # Then reconnect MQTT
                self.mqtt_client.reconnect()
                print("Successfully reconnected to MQTT")
                return True
            except Exception as e:
                attempt += 1
                print(f"MQTT reconnection attempt {attempt} failed: {e}")
                if attempt >= max_attempts:
                    print("Failed to reconnect to MQTT after multiple attempts")
                    return False
                time.sleep(2)  # Wait before retrying
        return False
