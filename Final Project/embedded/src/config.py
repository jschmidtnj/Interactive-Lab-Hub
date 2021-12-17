#!/usr/bin/env python3

import os
from typing import Optional
from dotenv import load_dotenv

WEATHER_ENDPOINT: Optional[str] = None
AUTH_TOKEN: Optional[str] = None

def load_config() -> None:
    global WEATHER_ENDPOINT
    global AUTH_TOKEN

    load_dotenv()

    WEATHER_ENDPOINT = os.environ.get("WEATHER_ENDPOINT")
    if not WEATHER_ENDPOINT:
        raise ValueError("cannot find weather endpoint")
    AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
    if not AUTH_TOKEN:
        raise ValueError("cannot find access secret")
