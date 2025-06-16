# wifi_setup.py
import board
import wifi
import socketpool
import ssl
import time

class WiFi():

    def __init__(self):
        # Get wifi details from settings.py
        try:
            from settings import settings
        except ImportError:
            print("WiFi settings are kept in settings.py, please add or change them there!")
            raise
        
        self.settings = settings
        
        # Connect to WiFi using Pico 2W's built-in WiFi
        print("Connecting to WiFi...")
        
        # Try to connect with a timeout and retry mechanism
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                wifi.radio.connect(self.settings["ssid"], self.settings["password"])
                print("Connected!")
                print("IP address:", wifi.radio.ipv4_address)
                break
            except (OSError, RuntimeError) as e:
                retry_count += 1
                print(f"Connection attempt {retry_count} failed: {e}")
                if retry_count >= max_retries:
                    print("Failed to connect to WiFi after multiple attempts")
                    # If we can't connect, we'll raise the exception
                    # This will allow the ecosystem to handle the error gracefully
                    raise
                time.sleep(2)  # Wait before retrying
        
        # Create socket pool for network connections
        self.pool = socketpool.SocketPool(wifi.radio)
        self.ssl_context = ssl.create_default_context()
        
    def reset(self):
        print("Reconnecting to WiFi...")
        try:
            # Disconnect first to ensure clean reconnection
            if wifi.radio.connected:
                wifi.radio.stop_station()
                time.sleep(1)
            
            # Then reconnect
            wifi.radio.connect(self.settings["ssid"], self.settings["password"])
            print("Reconnected to WiFi!")
        except (OSError, RuntimeError) as e:
            print(f"WiFi reconnection failed: {e}")
            # We don't raise here, to avoid crashing the application
            # The MQTT client will retry on its own