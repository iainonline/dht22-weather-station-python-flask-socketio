from RPLCD.i2c import CharLCD
from time import sleep
import smbus

def scan_i2c(bus_number=1):
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
    print(f"Attempting to initialize LCD at address 0x{address:02X}...")
    try:
        lcd = CharLCD('PCF8574', address, auto_linebreaks=True, backlight_enabled=True)
        print("LCD initialized successfully.")
        lcd.clear()
        lcd.write_string("LCD Test: Line 1")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Backlight ON")
        sleep(2)
        print("Turning backlight OFF for 2 seconds...")
        lcd.backlight_enabled = False
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Backlight OFF")
        sleep(2)
        print("Turning backlight ON.")
        lcd.backlight_enabled = True
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Backlight ON ")
        sleep(2)
        lcd.clear()
        lcd.write_string("Test complete!")
        print("LCD test complete. Check your display.")
        sleep(2)
        lcd.clear()
    except Exception as e:
        print(f"LCD test failed: {e}")

if __name__ == "__main__":
    found = scan_i2c()
    if 0x27 in found:
        lcd_test(0x27)
    else:
        print("LCD not found at 0x27. Please check wiring and power.")