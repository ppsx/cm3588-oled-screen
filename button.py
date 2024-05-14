# -*- coding: utf-8 -*-

import platform


# for CM3588
if platform.machine() == 'aarch64':
    import time
    import struct
    from threading import Thread

    is_pressed = False


    def wait_for_event():
        global is_pressed
        with open(f'/dev/input/by-path/platform-gpio-keys-event', "rb") as event:
            while True:
                raw_data = event.read(24)
                data = struct.unpack('4IHHI', raw_data)
                if data[4] == 1 and data[6] == 1:
                    is_pressed = True
                time.sleep(0.1)

    button_thread = Thread(target=wait_for_event)
    button_thread.start()

    def is_key_pressed():
        global is_pressed
        to_return = is_pressed
        is_pressed = False
        return to_return

# for development
elif platform.machine() == 'x86_64':
    from pynput import keyboard

    class KeyListener:
        def __init__(self):
            self.key_pressed = False
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

        def on_press(self, _):
            self.key_pressed = True

        def is_key_pressed(self):
            if self.key_pressed:
                self.key_pressed = False
                return True
            return False

    listener = KeyListener()

    def is_key_pressed():
        return listener.is_key_pressed()

# for other platforms
else:
    def is_key_pressed():
        return False
