# -*- coding: utf-8 -*-

from luma.core.render import canvas
from psutil._common import bytes2human


def draw_cpu(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "CPU", fill="white")

        if data is None:
            return

        draw.text((75, 3), "%-5.1f%%" % (data['percent'],), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * data['percent'] / 100), 120, 60), outline="white", fill="white")

        for i, cpu in enumerate(data['per_cpu']):
            draw.rectangle((
                5 + 50 * (0 if i < 4 else 1),
                25 + 10 * (i % 4),
                45 + 50 * (0 if i < 4 else 1),
                30 + 10 * (i % 4)),
                outline="white", fill="black", width=1)
            draw.rectangle((
                5 + 50 * (0 if i < 4 else 1),
                25 + 10 * (i % 4),
                5 + 50 * (0 if i < 4 else 1) + 40 * cpu / 100,
                30 + 10 * (i % 4)),
                outline="white", fill="grey")


def draw_mem(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "MEM", fill="white")

        if data is None:
            return

        draw.text((75, 3), "%-5.1f%%" % (data['memory'].percent,), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * data['memory'].percent / 100), 120, 60), outline="white", fill="white")

        draw.text((3, 15), "Mem total:", fill="white")
        draw.text((75, 15), "%s" % bytes2human(data['memory'].total), fill="white")
        draw.text((3, 25), "Mem free:", fill="white")
        draw.text((75, 25), "%s" % bytes2human(data['memory'].free), fill="white")

        draw.text((3, 35), "Swap total:", fill="white")
        draw.text((75, 35), "%s" % bytes2human(data['swap'].total), fill="white")
        draw.text((3, 45), "Swap used:", fill="white")
        draw.text((75, 45), "%s" % bytes2human(data['swap'].used), fill="white")


def draw_ssd(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "SSD", fill="white")

        if data is None:
            return

        draw.text((75, 3), "%-5.1f%%" % (data['storage'].percent,), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * data['storage'].percent / 100), 120, 60), outline="white", fill="white")

        draw.text((3, 15), "Storage total:", fill="white")
        draw.text((75, 15), "%s" % bytes2human(data['storage'].total), fill="white")
        draw.text((3, 25), "Storage free:", fill="white")
        draw.text((75, 25), "%s" % bytes2human(data['storage'].free), fill="white")

        draw.text((3, 35), "System total:", fill="white")
        draw.text((75, 35), "%s" % bytes2human(data['system'].total), fill="white")
        draw.text((3, 45), "System free:", fill="white")
        draw.text((75, 45), "%s" % bytes2human(data['system'].free), fill="white")


def draw_net(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "NET", fill="white")

        if data is None:
            return

        draw.text((50, 3), "%s" % (data['interface'],), fill="white")

        draw.text((3, 15), "IP:", fill="white")
        draw.text((50, 15), "%s" % data['ip'], fill="white")
        draw.text((3, 25), "Conn:", fill="white")
        draw.text((50, 25), "%s" % data['conn'], fill="white")

        draw.text((3, 35), "Downld:", fill="white")
        draw.text((50, 35), "%s/s" % bytes2human(data['in']), fill="white")
        draw.text((3, 45), "Upload:", fill="white")
        draw.text((50, 45), "%s/s" % bytes2human(data['out']), fill="white")


mapping = {
    'cpu': draw_cpu,
    'mem': draw_mem,
    'ssd': draw_ssd,
    'net': draw_net
}
