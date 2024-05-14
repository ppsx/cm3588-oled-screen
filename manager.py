# -*- coding: utf-8 -*-

import time
import probes
from threading import Timer, Thread, Event


class Manager:
    def __init__(self, dev, timeout=60):
        self._device = dev
        self._states = probes.mapping
        self._idx = 0
        self._timeout = timeout
        self._timer = None
        self._harvester = None
        self._data = {}
        self.to_stop = Event()
        self._new_data = False

    def _reset_state(self):
        self._idx = 0

    @property
    def state(self):
        return 'off' if self._idx == 0 else self._states[self._idx - 1][0]

    def next_state(self):
        if len(self._states) > 0:
            if self._idx == 0:
                self._idx = 1
            else:
                self._idx = (self._idx % len(self._states)) + 1
            probes.clear_previous()
            self.harvester_start()

    def off(self):
        self.timeout_stop()
        self._device.hide()
        self._reset_state()

    def timeout_start(self):
        self.timeout_stop()
        self._timer = Timer(self._timeout, self.off)
        self._timer.start()

    def timeout_stop(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def harvester_start(self):
        self.harvester_stop()
        self.timeout_start()
        self.to_stop.clear()
        self._device.clear()
        self._device.show()
        self._harvester = Thread(target=self._harvest, args=(self.to_stop,))
        self._harvester.start()

    def harvester_stop(self):
        if self._harvester is not None:
            self.to_stop.set()
            self._harvester.join()
            self._harvester = None

    def _harvest(self, to_stop):
        while True:
            if to_stop.is_set():
                break
            self._data[self.state] = self._states[self._idx - 1][1]()
            self._new_data = True
            time.sleep(1)   # 1 second because of counting the network speed (in/out per second)

    def cleanup(self):
        self.timeout_stop()
        self.harvester_stop()
        self.off()
        self._device.cleanup()

    def get_data(self):
        data = (self.state, self._new_data, self._data[self.state] if self.state in self._data else (self.state, None))
        self._new_data = False
        return data
