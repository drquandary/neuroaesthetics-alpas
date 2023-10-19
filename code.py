import board
import adafruit_bh1750
import busio
import digitalio
import time
import adafruit_requests
import socketpool
import ssl
import wifi
import json

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

def wait_5m(next_time: time.struct_time) -> time.struct_time:
    year, mon, day, hour, min, sec, day_of_wk, day_of_yr, _ = next_time
    sec = 0
    min = ((min // 2) + 1) * 2
    next_time = time.struct_time(
        (year, mon, day, hour, min, sec, day_of_wk, day_of_yr, -1)
    )
    time.sleep(max(0, time.mktime(next_time) - time.mktime(time.localtime())))
    return next_time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

gnd = digitalio.DigitalInOut(board.IO33)
gnd.direction = digitalio.Direction.OUTPUT
gnd.value = False

vin = digitalio.DigitalInOut(board.IO1)
vin.direction = digitalio.Direction.OUTPUT
vin.value = True

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bh1750.BH1750(i2c, 0x23)

sslctx = ssl.create_default_context()

while True:
    try:
        print("Connecting to WiFi...")
        wifi.radio.connect(secrets["ssid"], secrets["wifi_pw"])
        print("    Done! Sensor IP address:", wifi.radio.ipv4_address)

        pool = socketpool.SocketPool(wifi.radio)
        session = adafruit_requests.Session(pool, sslctx)

        next_time = time.localtime()

        while True:
            next_time = wait_5m(next_time)
            led.value = True
            sensor_data = "{:8.2f} lux".format(sensor.lux)
            print(sensor_data)

            # Send data to Flask server
            payload = {'light_value': sensor_data}
            response = session.post('YOURSERVERADDRESS:5000/sensor', json=payload)
            print('Server Response:', response.text)

            next_time = wait_5m(next_time)
            led.value = False

    except Exception as e:
        print(e)
        time.sleep(5)

