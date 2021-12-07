#!/usr/bin/env python3
from loguru import logger
from accel import is_spinning
from weather import Weather
from rpi_ws281x import Adafruit_NeoPixel, Color
from typing import Dict, Optional, cast
from time import sleep
from colormath.color_objects import sRGBColor
from webcolors import hex_to_rgb

LED_STRIP: Optional[Adafruit_NeoPixel] = None

LED_COUNT = 404  # Number of LED pixels.
LED_PIN = 21  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

def rgb_to_color(hex_str: str) -> sRGBColor:
    """
    convert rgb string to color object
    """
    color = hex_to_rgb(hex_str)
    return sRGBColor(color.red, color.green, color.blue)

WeatherColors: Dict[Weather, sRGBColor] = {
    Weather.Rain: rgb_to_color('#53789e'),
    Weather.Snow: rgb_to_color('#f2f3f4'),
    Weather.Extreme: rgb_to_color('#ed1c24'),
    Weather.Cloudy: rgb_to_color('#c4d3d4'),
    Weather.Clear: rgb_to_color('#f2d16b'),
}

def setup_lights() -> Adafruit_NeoPixel:
    global LED_STRIP
    LED_STRIP = Adafruit_NeoPixel(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )
    return LED_STRIP


def wheel(pos: int) -> Color:
    """
    Generate rainbow colors across 0-255 positions
    """
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(iterations: int = 1, wait_ms: int = 20) -> None:
    global LED_STRIP
    led_strip = cast(Adafruit_NeoPixel, LED_STRIP)

    for j in range(256 * iterations):
        for i in range(led_strip.numPixels()):
            led_strip.setPixelColor(i, wheel((i + j) & 255))
        led_strip.show()
        sleep(wait_ms / 1000.0)


def set_color(color: Color) -> None:
    """
    set color to a given color
    """
    global LED_STRIP
    led_strip = cast(Adafruit_NeoPixel, LED_STRIP)
    
    for i in range(led_strip.numPixels()):
        led_strip.setPixelColor(i, color)
    led_strip.show()


def clear() -> None:
    set_color(Color(0, 0, 0))


def fade_color(color: sRGBColor, fade_out: bool = True, wait_ms: int = 5) -> bool:
    """
    pulse in color
    """
    logger.debug('start fade')
    num_steps = 256
    for i in range(num_steps):
        scale = i / float(num_steps)
        current_color = Color(int(color.rgb_r * scale),
                                int(color.rgb_g * scale),
                                int(color.rgb_b * scale))
        set_color(current_color)
        sleep(wait_ms / 1000.)
        if is_spinning():
            return True
    if fade_out:
        for i in range(num_steps, 0, -1):
            scale = i / float(num_steps)
            current_color = Color(int(color.rgb_r * scale),
                                    int(color.rgb_g * scale),
                                    int(color.rgb_b * scale))
            set_color(current_color)
            sleep(wait_ms / 1000.)
            if is_spinning():
                return True
    return False

if __name__ == '__main__':
    strip = setup_lights()
    strip.begin()
    clear()
    sleep(1)
    # fade_color(WeatherColors[Weather.Rain])
    rainbow()
