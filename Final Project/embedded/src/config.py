#!/usr/bin/env python3

import os
from typing import Optional
from dotenv import load_dotenv

WEATHER_ENDPOINT: Optional[str] = None
ACCESS_SECRET: Optional[str] = None

def load_config() -> None:
    global WEATHER_ENDPOINT
    global ACCESS_SECRET

    load_dotenv()

    WEATHER_ENDPOINT = os.environ.get("WEATHER_ENDPOINT")
    if not WEATHER_ENDPOINT:
        raise ValueError("cannot find weather endpoint")
    ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
    if not ACCESS_SECRET:
        raise ValueError("cannot find access secret")
