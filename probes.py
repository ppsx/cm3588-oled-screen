# -*- coding: utf-8 -*-

import platform
import psutil as ps
from collections import namedtuple


if platform.machine() == 'aarch64':
    NETWORK_INTERFACE = 'eth0'
elif platform.machine() == 'x86_64':
    NETWORK_INTERFACE = 'wlp46s0'
else:
    NETWORK_INTERFACE = 'eth0'


def cpu_stat():
    return {
        'percent': ps.cpu_percent(),
        'per_cpu': [int(p) for p in ps.cpu_percent(percpu=True)],
    }


def mem_stat():
    data_mem = ps.virtual_memory()
    Mem = namedtuple('memusage', ['total', 'free', 'percent'])
    mem = Mem(data_mem.total, data_mem.available, data_mem.percent)
    data_swap = ps.swap_memory()
    Swap = namedtuple('swapusage', ['total', 'used'])
    swap = Swap(data_swap.total, data_swap.used)
    return {
        'memory': mem,
        'swap': swap
    }


def ssd_stat():
    # for CM3588
    # assume that all NVME SSDs are mounted under /srv and / is mounted either on SD card or eMMC
    if platform.machine() == 'aarch64':
        storage_prefix = '/srv/'
    # for development
    elif platform.machine() == 'x86_64':
        storage_prefix = '/backup'
    # for other platforms
    else:
        storage_prefix = '/tmp'

    storage_data = [ps.disk_usage(p.mountpoint) for p in ps.disk_partitions()
                    if p.mountpoint.startswith(storage_prefix)]
    Storage_Summary = namedtuple('sdiskusage', ['total', 'used', 'free', 'percent'])
    storage_summary = Storage_Summary(
        total=sum([p.total for p in storage_data]),
        used=sum([p.used for p in storage_data]),
        free=sum([p.free for p in storage_data]),
        percent=sum([p.percent for p in storage_data]) / len(storage_data),
    )
    return {
        'system': ps.disk_usage('/'),
        'storage': storage_summary,
    }


net_prev = {
    'in': 0,
    'out': 0
}


def net_stat():
    curr = ps.net_io_counters()
    ci = 0 if net_prev['in'] == 0 else curr.bytes_recv - net_prev['in']
    co = 0 if net_prev['out'] == 0 else curr.bytes_sent - net_prev['out']
    net_prev['in'] = curr.bytes_recv
    net_prev['out'] = curr.bytes_sent
    return {
        'interface': NETWORK_INTERFACE,
        'ip': ps.net_if_addrs()[NETWORK_INTERFACE][0].address,
        'conn': ps.net_if_stats()[NETWORK_INTERFACE].speed,
        'in': ci,
        'out': co
    }


mapping = (
    ('cpu', cpu_stat),
    ('mem', mem_stat),
    ('ssd', ssd_stat),
    ('net', net_stat)
)


def clear_previous():
    net_prev['in'] = 0
    net_prev['out'] = 0
