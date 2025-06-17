import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime, timezone
from dht22_module import DHT22Module
import board
from RPLCD.i2c import CharLCD

# if __name__ == "__main__":
#     socketio.run(app, port=5000, host="0.0.0.0", debug=True)

# Set your LCD address and bus
LCD_ADDRESS = 0x27  # Use your detected address
LCD_PORT = 1        # Usually 1 on Raspberry Pi

# Initialize the LCD
lcd = CharLCD(i2c_expander='PCF8574', address=LCD_ADDRESS, port=LCD_PORT, cols=16, rows=2, auto_linebreaks=True, backlight_enabled=True)

dht22_module = DHT22Module(board.D18)

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config["SECRET_KEY"] = "donsky!"
socketio = SocketIO(app)

"""
Background Thread
"""


def background_thread():
    while True:
        temperature_c, humidity = dht22_module.get_sensor_readings()
        temperature_f = (temperature_c * 9/5) + 32
        sensor_readings = {
            "temperature": temperature_f,
            "humidity": humidity,
            "timestamp": datetime.now(timezone.utc).isoformat()  # ISO 8601 format is ideal for JS charts
        }
        sensor_json = json.dumps(sensor_readings)
        socketio.emit("updateSensorData", sensor_json)
        display_on_lcd(temperature_c, humidity)
        # wait for 15 seconds
        socketio.sleep(15)

"""
Serve root index file
"""


@app.route("/")
def index():
    return render_template("index.html")


"""
Decorator for connect
"""


@socketio.on("connect")
def connect():
    global thread
    print("Client connected")

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


"""
Decorator for disconnect
"""


@socketio.on("disconnect")
def disconnect():
    print("Client disconnected", request.sid)

def display_on_lcd(temperature_c, humidity):
    # Convert Celsius to Fahrenheit
    temperature_f = (temperature_c * 9/5) + 32
    # Get current time and date
    now = datetime.now().strftime("%H:%M")
    today = datetime.now().strftime("%m/%d/%y")
    # Line 1: Temp left, time right (with 4 spaces before time)
    line1 = f"T:{temperature_f:.1f}F    {now}"
    line1 = line1[:16]
    # Line 2: Humidity (1 decimal place) left, date right
    hum_str = f"H:{humidity:.1f}%"
    # Calculate spaces to right-align the date after humidity
    spaces = 16 - len(hum_str) - len(today)
    line2 = hum_str + (" " * spaces) + today
    line2 = line2[:16]
    # Clear and write to LCD
    lcd.clear()
    lcd.write_string(line1)
    lcd.cursor_pos = (1, 0)
    lcd.write_string(line2)
