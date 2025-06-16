import time
import wifi

# Get MAC address
mac_bytes = wifi.radio.mac_address
mac_address = ":".join(["{:02x}".format(b) for b in mac_bytes])
print(f"MAC address: {mac_address}")

# Scan for networks
print("\nScanning for WiFi networks...")
networks = wifi.radio.start_scanning_networks()
for network in networks:
    print(f"SSID: {network.ssid}, RSSI: {network.rssi} dB, Channel: {network.channel}")
wifi.radio.stop_scanning_networks()
print("Scan complete")