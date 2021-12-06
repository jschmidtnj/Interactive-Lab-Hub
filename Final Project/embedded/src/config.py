#!/usr/bin/env python3

import os
from typing import Optional
from dotenv import load_dotenv

OPEN_WEATHER_MAP_API_KEY: Optional[str] = None


def load_config() -> None:
    global OPEN_WEATHER_MAP_API_KEY

    load_dotenv()
    OPEN_WEATHER_MAP_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
    if not OPEN_WEATHER_MAP_API_KEY:
        raise ValueError("cannot find open weather map api key")
