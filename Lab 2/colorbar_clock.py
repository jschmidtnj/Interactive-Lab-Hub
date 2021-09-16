#!/usr/bin/env python3
from datetime import datetime
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

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

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font_location = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    max_width = width - 25
    y = top
    now = datetime.now()

    x = 0
    hour_width = now.hour / 24 * max_width
    draw.rectangle((x, y, hour_width, 40), outline=0, fill="#1b95f2")
    x = hour_width + 5
    hour_text = now.strftime("%I")
    font = ImageFont.truetype(font_location, 40)
    draw.text((x, y), hour_text, font=font, fill="#FFFFFF")
    y += font.getsize(hour_text)[1]

    x = 0
    minute_width = now.minute / 60 * max_width
    draw.rectangle((x, y, minute_width, 60), outline=0, fill="#e05b0d")
    x = minute_width + 5
    minute_text = str(now.minute)
    font = ImageFont.truetype(font_location, 24)
    draw.text((x, y), minute_text, font=font, fill="#FFFFFF")
    y += font.getsize(minute_text)[1]

    x = 0
    second_width = now.second / 60 * max_width
    draw.rectangle((x, y, second_width, 60), outline=0, fill="#e05b0d")
    x = second_width + 5
    second_text = str(now.second)
    font = ImageFont.truetype(font_location, 24)
    draw.text((x, y), second_text, font=font, fill="#FFFFFF")
    y += font.getsize(second_text)[1]

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)

