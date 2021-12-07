#!/usr/bin/env python3
from typing import Optional, cast
from adafruit_mpu6050 import MPU6050
from board import SCL, SDA
from busio import I2C
from datetime import timedelta
from loguru import logger

PICKUP_THRESHOLD: float = 2.0
SPIN_THRESHOLD: float = 4.0
PICKUP_DELTA: timedelta = timedelta(seconds=2)
SPIN_DELTA: timedelta = timedelta(seconds=2)

MPU: Optional[MPU6050] = None


def setup_imu() -> None:
    global MPU
    i2c = I2C(SCL, SDA)
    MPU = MPU6050(i2c)


def picked_up() -> bool:
    global MPU
    mpu = cast(MPU6050, MPU)
    accel = sum([abs(elem) for elem in [mpu.acceleration[0], mpu.acceleration[2]]])
    logger.info(f'accel: {mpu.acceleration}')
    return accel > PICKUP_THRESHOLD


def is_spinning() -> bool:
    global MPU
    mpu = cast(MPU6050, MPU)
    return abs(mpu.acceleration[0]) > SPIN_THRESHOLD
