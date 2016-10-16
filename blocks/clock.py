#!/usr/bin/env python3

from ..block import Block

import datetime

class Clock(Block):
    def __init__(self, fmt='%a, %d %b %Y, %W week, %H:%M:%S', *args, **kwargs):
        Block.__init__(self, update_interval=1, *args, **kwargs)
        self._fmt = fmt

    def update(self):
        print('Clock.update')
        t = datetime.datetime.now()
        return t.strftime(self._fmt)
