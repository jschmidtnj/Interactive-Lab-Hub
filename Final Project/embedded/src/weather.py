#!/usr/bin/env python3

import requests
from http import HTTPStatus
from weather_enum import Weather


def get_weather() -> Weather:
    from config import ACCESS_SECRET, WEATHER_ENDPOINT

    # TODO - add current location (latitude longitude) in params
    res = requests.get(
        WEATHER_ENDPOINT,
        params={
            "token": ACCESS_SECRET,
        },
    )
    if res.status_code != HTTPStatus.OK:
        raise RuntimeError("cannot get weather data")
    data = res.json()

    weather: Weather = data["weather"]

    return weather
