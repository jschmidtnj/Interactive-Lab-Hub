import paho.mqtt.client as mqtt
import qwiic_joystick
import sys
import uuid

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

myJoystick = qwiic_joystick.QwiicJoystick()

if myJoystick.connected == False:
    print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    exit()

myJoystick.begin()

print(f"Initialized. Firmware Version: {myJoystick.version}")

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

while True:
    topic = f"IDD/joystick_test"
    data = f"X: {myJoystick.horizontal}, Y: {myJoystick.vertical}, Button: {myJoystick.button}"
    client.publish(topic, data)
