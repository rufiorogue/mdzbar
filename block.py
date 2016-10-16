#!/usr/bin/env python3

import threading
import functools
from mdzbar.eventhook import EventHook

__all__ = ['Block']

class Block:
    '''
    @variable align:left,center,right   Alignment of the block within the bar

    @variable padding:(left,right)      Space between text and block edge.
                                        NOTE: space between adjacent blocks should
                                        be modeled with a spacer block instead.

    @variable update_interval:float     Update interval in seconds. If zero,
                                        then updated only once
    '''
    def __init__(self, bg=None, fg=None, align='right', padding=(0,0),
                 update_interval=2):
        self._message = ''
        self._bg = bg
        self._fg = fg
        self._align = align
        self._padding = padding
        self._interval = update_interval
        self._active = True
        self._timer = None
        self.on_changed = EventHook()


    '''
    Once activated, the block begins calling update() and emitting Changed events
    '''
    def activate(self):
        self._active =True
        # schedule first process() to be called ASAP
        self._timer = threading.Timer(0, functools.partial(Block._process, self))
        self._timer.start()

    '''
    Deactivated block will not update its content
    '''
    def deactivate(self):
        self._active = False
        if self._timer:
            self._timer.cancel()


    def _process(self):
        content = ''
        if self._bg:
            content += '^bg(' + self._bg + ')'
        if self._fg:
            content += '^fg(' + self._fg + ')'
        for i in range(0, self._padding[0]):
            content += ' '

        # update() is defined in derived classes
        content += self.update()

        for i in range(0, self._padding[1]):
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
