#!/usr/bin/env python3
from typing import Optional, cast
from adafruit_mpu6050 import MPU6050
from board import SCL, SDA
from busio import I2C
from datetime import timedelta

PICKUP_THRESHOLD: float = 5.0
SPIN_THRESHOLD: float = 8.0
PICKUP_DELTA: timedelta = timedelta(seconds=5)
SPIN_DELTA: timedelta = timedelta(seconds=5)

MPU: Optional[MPU6050] = None


def setup_imu() -> None:
    global MPU
    i2c = I2C(SCL, SDA)
    MPU = MPU6050(i2c)


def picked_up() -> bool:
    global MPU
    mpu = cast(MPU6050, MPU)
    total_accel = sum(mpu.acceleration)
    return total_accel > PICKUP_THRESHOLD


def is_spinning() -> bool:
    global MPU
    mpu = cast(MPU6050, MPU)
    return mpu.acceleration[2] > SPIN_THRESHOLD
