#!/usr/bin/env python3

from weather import Weather, get_weather
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
        weather_escape = False
        pickup_ready = last_picked_up + PICKUP_DELTA < datetime.now() and picked_up()
        if pickup_ready:
            last_picked_up = datetime.now()
            # weather = get_weather()
            weather = Weather.Rain
            logger.debug(f'current weather: ${weather}')
            logger.debug(f'color: {WeatherColors[weather]}')
            weather_escape = fade_color(WeatherColors[weather])
            if not weather_escape:
                clear()
        if weather_escape or (not pickup_ready and (last_spin + SPIN_DELTA < datetime.now() and is_spinning())):
            logger.debug('detected spin')
            last_spin = datetime.now()
            rainbow()
            clear()
        sleep(1 / UPDATE_RATE)
