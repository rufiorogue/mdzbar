#!/usr/bin/env python3

import threading
import functools
from mdzbar.eventhook import EventHook

__all__ = ['Block']

class Block:
    '''
    @variable align:left,center,right   Alignment of the block within the bar
    @variable update_interval:float     Update interval in seconds. If zero,
                                        then updated only once
    '''
    def __init__(self, bg=None, fg=None, align='right', padding=0, update_interval=2):
        self._message = ''
        self._bg = bg
        self._fg = fg
        self._align = align
        self._padding = padding
        self._interval = update_interval
        self.on_changed = EventHook()
        self._active = True


    '''
    Once activated, the block begins calling update() and emitting Changed events
    '''
    def activate(self):
        self._process()

    def deactivate(self):
        self._active = False
        self._timer.cancel()


    def _process(self):
        content = ''
        if self._bg:
            content += '^bg(' + self._bg + ')'
        if self._fg:
            content += '^fg(' + self._fg + ')'
        for i in range(1, self._padding):
            content += ' '

        # update() is defined in derived classes
        content += self.update()

        for i in range(1, self._padding):
            content += ' '
        if self._bg:
            content += '^bg()'
        if self._fg:
            content += '^fg()'

        self._message = content

        self.on_changed.fire()

        # if we are not done yet, schedule a timer to be run that will
        # call _process() for us again
        if self._active and self._interval > 0:
            self._timer = threading.Timer(self._interval, 
                                          functools.partial(Block._process, self))
            self._timer.start()


    '''
    Get the formatted data for the block
    '''
    def __str__(self):
        return self._message

    '''
    @return string : block content
    Overridden
    '''
    def update(self):
        pass
