#!/usr/bin/env python3

from ..block import Block

import datetime

class Clock(Block):
    def __init__(self, fmt='%a %d %b %Y  %W.%w  %H:%M:%S', *args):
        Block.__init__(self, args)
        self._fmt = fmt
        self._interval = 1

    def update(self):
        print('Clock.update')
        t = datetime.datetime.now()
        return t.strftime(self._fmt)
