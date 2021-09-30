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

canvas_padding = -2
top = canvas_padding
bottom = height - canvas_padding
left = canvas_padding
right = width - canvas_padding
canvas_width = right - left
canvas_height = bottom - top

font_location = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

box_padding = 1

def draw_rectangles(num: int, out_of: int, height_frac: float, start_y: int, color: str) -> int:
    curr_x = left
    curr_y = start_y
    box_width = canvas_width / out_of - box_padding
    box_height = canvas_height * height_frac
    for i in range(num):
        draw.rectangle((curr_x, curr_y, curr_x + box_width, curr_y + box_height), outline=0, fill=color)
        curr_x += box_width + box_padding
    return curr_y + box_height + box_padding

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    now = datetime.now()

    curr_y = draw_rectangles(now.hour, 24, .35, top, "#1b95f2")
    curr_y = draw_rectangles(now.minute, 60, .4, curr_y, "#ff193c")
    draw_rectangles(now.second, 60, .25, curr_y, "#e05b0d")

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)

