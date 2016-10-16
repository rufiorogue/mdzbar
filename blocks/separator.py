#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#


from ..block import Block

class Separator(Block):
    def __init__(self, size=0, *args, **kwargs):
        Block.__init__(self, update_interval=0, *args, **kwargs)
        self._size = size

    def update(self):
        return '^p(%d)'%(self._size)
