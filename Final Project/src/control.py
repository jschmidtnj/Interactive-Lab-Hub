#!/usr/bin/env python3

from weather import get_weather
from accel import is_spinning, picked_up, PICKUP_DELTA, SPIN_DELTA
from time import sleep
from datetime import datetime
from lights import clear, rainbow, fade_color, WeatherColors
from loguru import logger

UPDATE_RATE: float = 1.0  # hz


def control_loop() -> None:
    clear()

    last_picked_up = datetime.now() - PICKUP_DELTA
    last_spin = datetime.now() - SPIN_DELTA
    while True:
        if last_spin + PICKUP_DELTA < datetime.now() and is_spinning():
            logger.debug('detected spin')
            last_spin = datetime.now()
            rainbow()
            clear()
        elif last_picked_up + PICKUP_DELTA < datetime.now() and picked_up():
            last_picked_up = datetime.now()
            weather = get_weather()
            logger.debug(f'current weather: ${weather}')
            fade_color(WeatherColors[weather])
            clear()
        sleep(1 / UPDATE_RATE)
