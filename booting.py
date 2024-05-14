# -*- coding: utf-8 -*-

import time
import subprocess
from luma.core.sprite_system import framerate_regulator
from PIL import Image, ImageSequence
from luma.core.render import canvas


def system_state():
    try:
        return subprocess.check_output(["/usr/bin/systemctl", "is-system-running"]).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8').strip()


def display_boot_logo(device):
    start_time = 0
    regulator = framerate_regulator(fps=10)
    img_path = 'loading-01b.gif'
    image = Image.open(img_path)

    is_running = True

    while is_running:
        for frame in ImageSequence.Iterator(image):
            with regulator:
                background = Image.new("RGB", device.size, "black")
                background.paste(frame, (0, 0))
                device.display(background.convert(device.mode))
                if system_state != 'starting':
                    if start_time == 0:
                        start_time = time.time()
                    if time.time() - start_time > 5:
                        is_running = False


def draw_ready(device):
    with canvas(device) as draw:
        draw.text((3, 3), "System ready", fill="white")


def booting(device):
    display_boot_logo(device)
    draw_ready(device)
