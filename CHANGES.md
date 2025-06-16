# Changes for Raspberry Pi Pico 2W Port

This document outlines the changes made to adapt the Great Interactive Reef project from the ItsyBitsy M4 + ESP32 to the Raspberry Pi Pico 2W.

## Major Changes

1. **WiFi Connectivity**
   - Replaced ESP32 SPI WiFi with Pico 2W's native WiFi
   - Updated `wifi_setup.py` to use CircuitPython's built-in `wifi` module
   - Added robust error handling and connection retry mechanisms
   - Simplified connection code by removing ESP32-specific configuration

2. **MQTT Integration**
   - Updated MQTT setup to work with Pico 2W's network stack
   - Added connection retry and failover to offline mode
   - Enhanced error handling throughout MQTT operations
   - Improved reconnection logic for network interruptions

3. **Pin Assignments**
   - Created a central `pin_config.py` file to make pin management easier
   - Updated all component files to use the centralized pin configuration
   - Remapped pins from ItsyBitsy to Pico 2W equivalent GPIO pins:

| Component       | Original ItsyBitsy M4 Pin | Pico 2W Pin |
|-----------------|---------------------------|-------------|
| Button          | A2                        | GP27        |
| Servo Motor     | D4                        | GP16        |
| Vibration Motor | D2                        | GP28        |
| NeoPixel LED    | D13                       | GP1         |
| Buzzer          | D7                        | GP7         |

4. **Improved Stability**
   - Added fallback to offline mode when network is unavailable
   - Created separate online/offline code examples
   - Added timeouts and retries for all network operations
   - Graceful error handling throughout the codebase

5. **Documentation**
   - Updated README.md with Pico 2W-specific information
   - Created this CHANGES.md file to document the port
   - Added settings_template.py as a reference for configuration

## Files Modified

- `lib/components/wifi_setup.py` - Complete rewrite for Pico 2W WiFi with robust error handling
- `lib/components/mqtt_setup.py` - Updated for Pico 2W network stack with connection retry
- `lib/components/button.py` - Updated pin and added pull-up resistor
- `lib/components/servo_motor.py` - Updated pin assignment
- `lib/components/vibration_motor.py` - Updated pin assignment
- `lib/components/neopixel_led.py` - Updated pin assignment
- `lib/components/buzzer.py` - Updated pin assignment
- `creature.py` - Updated pin references in comments
- `ecosystem.py` - Added error handling and offline fallback
- `code.py` - Changed default to online mode
- `README.md` - Added Pico 2W-specific information

## New Files Created

- `pin_config.py` - Central pin configuration
- `settings_template.py` - Template for WiFi and MQTT settings
- `code_offline.py` - Offline mode version for testing without WiFi
- `CHANGES.md` - This document

## Notes for Users

- Make sure to copy `settings_template.py` to `settings.py` and update with your credentials
- The Pico 2W's GPIO pins are laid out differently than the ItsyBitsy M4, so check pin diagrams when connecting hardware
- If WiFi connection fails, the system will automatically fall back to offline mode
- Use `code_offline.py` for testing hardware without a network connection
- All pin assignments can be modified in one place via `pin_config.py`