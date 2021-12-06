#!/usr/bin/env python3

import json
from http import HTTPStatus
from typing import Dict, Any
from preprocess.src.config import load_config
from preprocess.src.weather import get_weather


def hello(_event, _context) -> Dict[str, Any]:
    body: Dict[str, str] = {
        "message": "Hello World!"
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }


def handle_error(err: str, status: int) -> Dict[str, Any]:
    body: Dict[str, str] = {
        "error": err
    }

    return {
        "statusCode": status,
        "body": json.dumps(body)
    }


TOKEN_KEY: str = "token"

def data(event, _context):
    load_config()
    from config import AUTH_TOKEN

    if TOKEN_KEY not in event['queryStringParameters']:
        return handle_error("no access token found", HTTPStatus.UNAUTHORIZED)

    if event['queryStringParameters'][TOKEN_KEY] != AUTH_TOKEN:
        return handle_error("invalid access token provided", HTTPStatus.UNAUTHORIZED)

    weather = get_weather()
    body: Dict[str, int] = {
        "weather": weather
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
