
#!/usr/bin/env python3

from ..block import Block

class Separator(Block):
    def __init__(self, size=0, *args, **kwargs):
        Block.__init__(self, update_interval=0, *args, **kwargs)
        self._size = size

    def update(self):
        return '^p(%d)'%(self._size)
