#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from demo_opts import get_device
from manager import Manager
from button import is_key_pressed
from booting import booting
from screen import mapping

# from luma.core.interface.serial import i2c
# from luma.oled.device import ssd1306
#
# serial = i2c(port=8, address=0x3C)
# device = ssd1306(serial)


SCREEN_TIMEOUT = 60


def main():
    booting(device)
    manager.timeout_start()
    while True:
        while True:
            is_pressed = is_key_pressed()
            if is_pressed:
                break
            state, is_new, data = manager.get_data()
            if state != 'off' and is_new:
                # get new data and update screen
                try:
                    mapping[state](device, data)
                except Exception as e:
                    print(e)
            time.sleep(0.5)
        manager.next_state()


manager = None

if __name__ == "__main__":
    try:
        device = get_device()
        manager = Manager(device, timeout=SCREEN_TIMEOUT)
        main()
    except KeyboardInterrupt:
        if manager is not None:
            manager.cleanup()
        pass
