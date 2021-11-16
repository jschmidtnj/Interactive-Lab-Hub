import board
import busio
import adafruit_apds9960.apds9960
import time
import paho.mqtt.client as mqtt
import uuid
import signal

import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

height =  disp.height
width = disp.width 
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)


i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_color = True
r, g, b, a = sensor.color_data

topic = 'IDD/colors'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    # if a message is received on the colors topic, parse it and set the color
    if msg.topic == topic:
        colors = list(map(int, msg.payload.decode('UTF-8').split(',')))
        draw.rectangle((0, 0, width, height*0.5), fill=colors[0])
        disp.image(image)

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

# hen sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)

# our main loop
while True:
    time.sleep(.01)
