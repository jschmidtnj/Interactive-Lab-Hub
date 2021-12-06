#!/usr/bin/env python3
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import urllib.request # https://www.codespeedy.com/how-to-check-the-internet-connection-in-python/

print("Trying to connect to google.com.")
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        print("Ok I can find google.com")
        return True
    except:
        return False

count=0;


print("This script will try to print the IP and MAC address and the wifi name to a SPI screen.")
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    success=False
    try:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        success=connect()

        cmd = "ifconfig wlan0 | awk '/inet / {print $2}'"
        IP = "IP: " +(subprocess.check_output(cmd, shell=True).decode("utf-8") if success else "Waiting to connect")
        cmd = "ifconfig ppp0 | awk '/inet / {print $2}'"
        CELL = "cell IP: " +(subprocess.check_output(cmd, shell=True).decode("utf-8") if success else "Waiting to connect")
        cmd = "cat /sys/class/net/wlan0/address"
        MAC = 'MAC: ' + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "iwgetid -r"
        NET = 'NET: '+( subprocess.check_output(cmd, shell=True).decode("utf-8")  if success else "waiting to connect")
        MESSAGE = "LightBrella"
        # Write lines of text.
        y = top
        draw.text((x, y), MESSAGE, font=font, fill="#FF0000")
        y += font.getsize(MESSAGE)[1]
        draw.text((x, y), CELL, font=font, fill="#00FF00")
        y += font.getsize(CELL)[1]
        draw.text((x, y), IP, font=font, fill="#00FFFF")
        y += font.getsize(IP)[1]
        draw.text((x, y), NET, font=font, fill="#FFFFFF")
        y += font.getsize(NET)[1]
        draw.text((x, y), MAC, font=font, fill="#FFFF00")
        y += font.getsize(MAC)[1]

        # Display image.
        disp.image(image, rotation)
        time.sleep(1.0)
        print("Success we finished writing to the screen")
        if success:
            print("I am done here!")
            break
    except:
        print("Something did not work.")
        time.sleep(1.0)
