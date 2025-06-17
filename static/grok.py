import smbus2 as smbus
from RPLCD.i2c import CharLCD
from time import sleep

def scan_i2c(bus_number=1):
    """Scan I2C bus for connected devices."""
    print("Scanning I2C bus for devices...")
    bus = smbus.SMBus(bus_number)
    found = []
    for address in range(0x03, 0x78):
        try:
            bus.write_quick(address)
            print(f"Found device at 0x{address:02X}")
            found.append(address)
        except OSError:
            continue
    if not found:
        print("No I2C devices found.")
    return found

def lcd_test(address=0x27, bus_number=1):
    """Test LCD display by initializing and writing text."""
    print(f"Attempting to initialize LCD at address 0x{address:02X}...")
    try:
        # Initialize LCD with explicit parameters
        lcd = CharLCD(
            i2c_expander='PCF8574',
            address=address,
            port=bus_number,
            cols=16,  # Adjust to your LCD's column count (e.g., 16x2 LCD)
            rows=2,   # Adjust to your LCD's row count
            auto_linebreaks=True,
            backlight_enabled=True
        )
        print("LCD initialized successfully.")
        
        # Clear the display and ensure it's enabled
        lcd.clear()
        lcd.display_enabled = True
        
        # Set cursor to home position (0,0)
        lcd.cursor_pos = (0, 0)
        print("Sending text to LCD...")
        
        # Write text to the first line
        lcd.write_string("LCD Test: Line 1")
        
        # Move cursor to second line (if your LCD has multiple lines)
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Line 2: Works!")
        
        # Ensure the buffer is flushed
        lcd._write_cmd(0x01)  # Explicitly clear display to flush
        print("Text sent to LCD. Display should show text.")
        
        # Keep display on for 10 seconds
        sleep(10)
        
        # Turn off backlight to confirm control
        lcd.backlight_enabled = False
        print("Backlight turned off.")
        
    except Exception as e:
        print(f"LCD test failed: {e}")

if __name__ == "__main__":
    # Scan for I2C devices
    found = scan_i2c()
    if 0x27 in found:
        lcd_test(0x27)
    else:
        print("LCD not found at 0x27. Please check wiring, power, or I2C address.")