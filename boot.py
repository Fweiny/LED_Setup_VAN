
import network
import socket
import machine
import time

print('---------------------')
print('ESP - Boooting')
print('---------------------')
print('FW')
print('Version ---> PWM')
print('Three buttin version')



# Set up the WiFi hotspot
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='MyESP32', password='mypassword')

# Set up the web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Define the HTML page
html = """<html>
<head>
    <title>ESP32 Light Control</title>
    <style>
        body {
            font-size: 24px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        button {
            font-size: 24px;
            padding: 10px;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <h1>ESP32 Light Control</h1>
    <form method="get" action="/">
        <label for="led1">LED 1:</label>
        <button id="led1_on" name="led1" value="on">On</button>
        <button id="led1_off" name="led1" value="off">Off</button>
        <br><br>
        <label for="led2">LED 2:</label>
        <button id="led2_on" name="led2" value="on">On</button>
        <button id="led2_off" name="led2" value="off">Off</button>
        <br><br>
        <label for="led3">LED 3:</label>
        <button id="led3_on" name="led3" value="on">On</button>
        <button id="led3_off" name="led3" value="off">Off</button>
        <br><br>
        <div style="margin-top: 50px;">
            <label for="all">All LEDs:</label>
            <button id="all_on" name="all" value="on">On</button>
            <button id="all_off" name="all" value="off">Off</button>
        </div>
        <br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>"""


print('HTML started')