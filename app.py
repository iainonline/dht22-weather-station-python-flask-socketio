import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime, timezone
from dht22_module import DHT22Module
import board

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


# if __name__ == "__main__":
#     socketio.run(app, port=5000, host="0.0.0.0", debug=True)
