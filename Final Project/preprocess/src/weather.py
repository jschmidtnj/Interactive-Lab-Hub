#!/usr/bin/env python3

import requests
from http import HTTPStatus
from collections import Counter
from weather_enum import Weather, WeatherMap

API_BASE = "https://api.openweathermap.org/data/2.5/onecall"


def get_weather() -> Weather:
    from config import OPEN_WEATHER_MAP_API_KEY

    res = requests.get(
        API_BASE,
        params={
            "exclude": ",".join(["daily", "minutely"]),
            "appid": OPEN_WEATHER_MAP_API_KEY,
            "lat": "40.7128",
            "lon": "-74.0060",
        },
    )
    if res.status_code != HTTPStatus.OK:
        raise RuntimeError("cannot get weather data")
    data = res.json()

    weather_counter = Counter()
    for curr_data in data["hourly"][:2]:
        curr_weather_str = curr_data["weather"][0]["main"]
        curr_weather = WeatherMap[curr_weather_str]
        if curr_weather == Weather.Rain:
            return curr_weather
        weather_counter.update([curr_weather])

    weather = weather_counter.most_common(1)[0][0]
    return weather
# :)
