#!/usr/bin/env python3

from weather import get_weather
from accel import is_spinning, picked_up, PICKUP_DELTA, SPIN_DELTA
from time import sleep
from datetime import time
from lights import rainbow, fade_color, WeatherColors
from loguru import logger

UPDATE_RATE: float = 1.0  # hz


def control_loop() -> None:
    last_picked_up = time() - PICKUP_DELTA
    last_spin = time() - SPIN_DELTA
    while True:
        if last_spin + PICKUP_DELTA < time() and is_spinning():
            last_spin = time()
            rainbow()
        elif last_picked_up + PICKUP_DELTA < time() and picked_up():
            last_picked_up = time()
            weather = get_weather()
            logger.debug(f'current weather: ${weather}')
            fade_color(WeatherColors[weather])
        sleep(1 / UPDATE_RATE)
