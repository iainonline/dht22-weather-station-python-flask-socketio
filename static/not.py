from RPLCD.i2c import CharLCD
from time import sleep
import smbus2 as smbus

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
        lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, auto_linebreaks=True, backlight_enabled=True)
        print("LCD initialized successfully.")
        lcd.clear()
        lcd.display_enabled = True
        print("Sending text to LCD...")
        lcd.write_string("LCD Test: Line 1")
        sleep(10)
    except Exception as e:
        print(f"LCD test failed: {e}")

if __name__ == "__main__":
    found = scan_i2c()
    if 0x27 in found:
        lcd_test(0x27)
    else:
        print("LCD not found at 0x27. Please check wiring and power.")