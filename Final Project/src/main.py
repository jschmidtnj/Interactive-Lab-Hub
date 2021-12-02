#!/usr/bin/env python3

from config import load_config
from accel import setup_imu
from control import control_loop
from lights import setup_lights


def main() -> None:
    load_config()
    setup_imu()
    strip = setup_lights()
    strip.begin()
    control_loop()


if __name__ == "__main__":
    main()
