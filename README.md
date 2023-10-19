# Penn Center for Neuroaesthetics Ambient Light Sensor with Simple Flask Server

Written in CircuitPython for ease of maintenance from across the country.

Currently tested on an Unexpected Maker Feather S3 & Adafruit BH1750 soldered so that `VIN 3Vo GND SCL SDA` on the BH1750 connects to `1 38 33 SCL SDA` on the Feather. Note that `ADDR` is left unsoldered and `3Vo`/`38` is unused but soldered anyway to avoid having to chop header pins in half.

## Setup
The device needs configuration. Look at CircuitPython docs for that and make sure to download MU. To send light data, the device will need to be coded to collect and send data and also a server to receive it. 

# Device Set up
Obtain a CircuitPython-compatible microcontroller and copy everything in this folder into it, overwriting where applicable. Then, add a `secrets.py` file that looks like this:
```python
secrets = {
    "ssid": "replace me with your WiFi network name",
    "wifi_pw": "replace me with your WiFi password",
    "email": "address@site.com"
    "password": "S3cureP@ssw0rd"
    "login_encrypted": "AGFkZHJlc3NAc2l0ZS5jb20AUzNjdXJlUEBzc3cwcmQ=" # See below the code snippet for an explanation!
    "host": "smtp.gmail.com",
    "port": 465, # Gmail's required SSL port
}
```
How did we get the value for `login_encrypted`?
In a terminal (not Python), type `echo -ne '\0{your username}\0{your password}' | base64`.
With the above email and password, it would be `echo -ne '\0address@site.com\0S3cureP@ssw0rd' | base64` (exactly, to the letter!), which should output `AGFkZHJlc3NAc2l0ZS5jb20AUzNjdXJlUEBzc3cwcmQ=`. Do this for your username and password, then copy it into the `login_encrypted` field.

And everything should work! The blue light should flash on or off every five minutes, alternating with each measurement.

To update to the newest version of our code, run `./update.sh`.

# Server Setup
1) Use a service like Digital Ocean with Ubuntu. Set up a venv with python and add the server script (server.py) with something like VIM.
2) Make sure no firewall is blocking the server.
3) Write down your server address and use this for the next stage

# Chip Data-collector 
1) Edit the data collector code in code.py to send data to your server's address: response = session.post('YOURSERVERADDRESS:5000/sensor', json=payload)
2) You can test this easily in MU using the serial function


