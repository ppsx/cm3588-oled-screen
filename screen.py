# -*- coding: utf-8 -*-

from luma.core.render import canvas
from psutil._common import bytes2human


def draw_cpu(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "CPU", fill="white")

        if data is None:
            return

        draw.text((75, 3), "%-5.1f%%" % (data['percent'], ), fill="white")

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

        draw.text((75, 3), "%-5.1f%%" % (data['memory'].percent, ), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * data['memory'].percent / 100), 120, 60), outline="white", fill="white")

        draw.text((3, 20), "Mem total:", fill="white")
        draw.text((75, 20), f"{bytes2human(data['memory'].total)}", fill="white")
        draw.text((3, 30), "Mem free:", fill="white")
        draw.text((75, 30), f"{bytes2human(data['memory'].free)}", fill="white")

        draw.text((3, 40), "Swap total:", fill="white")
        draw.text((75, 40), f"{bytes2human(data['swap'].total)}", fill="white")
        draw.text((3, 50), "Swap used:", fill="white")
        draw.text((75, 50), f"{bytes2human(data['swap'].used)}", fill="white")


def draw_ssd(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "SSD", fill="white")

        if data is None:
            return

        draw.text((75, 3), "%-5.1f%%" % (data['storage'].percent, ), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * data['storage'].percent / 100), 120, 60), outline="white", fill="white")

        draw.text((3, 20), "Storage total:", fill="white")
        draw.text((75, 20), f"{bytes2human(data['storage'].total)}", fill="white")
        draw.text((3, 30), "Storage free:", fill="white")
        draw.text((75, 30), f"{bytes2human(data['storage'].free)}", fill="white")

        draw.text((3, 40), "System total:", fill="white")
        draw.text((75, 40), f"{bytes2human(data['system'].total)}", fill="white")
        draw.text((3, 50), "System free:", fill="white")
        draw.text((75, 50), f"{bytes2human(data['system'].free)}", fill="white")


def draw_net(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "NET", fill="white")

        if data is None:
            return

        draw.text((50, 3), f"{data['interface']}", fill="white")

        draw.text((3, 20), "IP:", fill="white")
        draw.text((50, 20), f"{data['ip']}", fill="white")
        draw.text((3, 30), "Conn:", fill="white")
        draw.text((50, 30), f"{data['conn']}", fill="white")

        draw.text((3, 40), "Downld:", fill="white")
        draw.text((50, 40), f"{bytes2human(data['in'])}/s", fill="white")
        draw.text((3, 50), "Upload:", fill="white")
        draw.text((50, 50), f"{bytes2human(data['out'])}/s", fill="white")


def draw_temp_cpu(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "TEMP CPU", fill="white")

        if data is None:
            return

        dm = max(data['cpu0'], data['cpu1'], data['cpu2'], data['soc'])
        dp = dm/data['max']
        if dp > 1:
            dp = 1

        draw.text((75, 3), "%.1f\N{DEGREE SIGN}C" % (dm, ), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * dp), 120, 60), outline="white", fill="white")

        draw.text((3, 20), "CPU0:", fill="white")
        draw.text((75, 20), "%.1f\N{DEGREE SIGN}C" % (data['cpu0'], ), fill="white")
        draw.text((3, 30), "CPU1:", fill="white")
        draw.text((75, 30), "%.1f\N{DEGREE SIGN}C" % (data['cpu1'], ), fill="white")
        draw.text((3, 40), "CPU2:", fill="white")
        draw.text((75, 40), "%.1f\N{DEGREE SIGN}C" % (data['cpu2'], ), fill="white")
        draw.text((3, 50), "SOC:", fill="white")
        draw.text((75, 50), "%.1f\N{DEGREE SIGN}C" % (data['soc'], ), fill="white")


def draw_temp_ssd(device, data):
    with canvas(device) as draw:
        draw.text((3, 3), "TEMP NVME", fill="white")

        if data is None:
            return

        dm = max(data['nvme0'], data['nvme1'], data['nvme2'], data['nvme3'])
        dp = dm/data['max']
        if dp > 1:
            dp = 1

        draw.text((75, 3), "%.1f\N{DEGREE SIGN}C" % (dm, ), fill="white")

        draw.rectangle((110, 5, 120, 60), outline="white", fill="black", width=1)
        draw.rectangle((110, 60 - int(55 * dp), 120, 60), outline="white", fill="white")

        draw.text((3, 20), "NVME0:", fill="white")
        draw.text((75, 20), "%.1f\N{DEGREE SIGN}C" % (data['nvme0'], ), fill="white")
        draw.text((3, 30), "NVME1:", fill="white")
        draw.text((75, 30), "%.1f\N{DEGREE SIGN}C" % (data['nvme1'], ), fill="white")
        draw.text((3, 40), "NVME2:", fill="white")
        draw.text((75, 40), "%.1f\N{DEGREE SIGN}C" % (data['nvme2'], ), fill="white")
        draw.text((3, 50), "NVME3:", fill="white")
        draw.text((75, 50), "%.1f\N{DEGREE SIGN}C" % (data['nvme3'], ), fill="white")


mapping = {
    'cpu': draw_cpu,
    'mem': draw_mem,
    'ssd': draw_ssd,
    'net': draw_net,
    'temp_cpu': draw_temp_cpu,
    'temp_ssd': draw_temp_ssd
}
