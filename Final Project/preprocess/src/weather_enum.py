#!/usr/bin/env python3

from enum import Enum, auto
from typing import Dict


class Weather(Enum):
    Rain = auto
    Cloudy = auto
    Sunny = auto
    Snow = auto
    Extreme = auto
    Clear = auto


WeatherMap: Dict[str, Weather] = {
    "Rain": Weather.Rain,
    "Clouds": Weather.Cloudy,
    "Snow": Weather.Snow,
    "Clear": Weather.Clear,
    "Extreme": Weather.Extreme,
}
