# this works to turn off the backlight of the LCD1602 display

import smbus2 as smbus
import LCD1602
from time import sleep

def find_lcd_address(bus_number=1, possible_addresses=[0x27, 0x3F]):
    bus = smbus.SMBus(bus_number)
    for address in possible_addresses:
        try:
            bus.write_quick(address)
            print(f"Found LCD at I2C address 0x{address:02X}")
            return address
        except OSError:
            continue
    print("No LCD found at common addresses.")
    return None

# Detect and set the LCD address at import time
lcd_address = find_lcd_address()

if lcd_address is not None:
    print(f"LCD address set to 0x{lcd_address:02X}")
else:
    print("LCD address not set. Please check wiring and power.")

# turn off the LCD backlight
bus = smbus.SMBus(1)
bus.write_byte(lcd_address, 0x00)
print('backlight off')

sleep(2)

# create LCD1602 instance
LCD1602 = LCD1602.CharLCD1602()
LCD1602.LCD_ADDR = lcd_address

# turn on the LCD backlight
LCD1602.BLEN = 1
print('backlight on')

sleep(2)

# turn off the LCD backlight
LCD1602.BLEN = 0



sleep(10)
print("Program has finished executing")