#!/usr/bin/env python3

import threading
import functools
from mdzbar.eventhook import EventHook

__all__ = ['Block']

class Block:

    ''' Default padding '''
    default_padding=(0,0)

    ''' Default update interval '''
    default_update_interval=2

    ''' Background color attribute used with blink effect '''
    blink_bg='red'

    ''' Blink interval in seconds '''
    blink_interval=0.5

    '''
    @variable align:left,center,right   Alignment of the block within the bar

    @variable padding:(left,right)      Space in chars between text and block edge.
                                        -NOTE1- padding cannot be specified in pixels
                                        because dzen2 applies color attributes
                                        only to text content.
                                        -NOTE2- space between adjacent blocks should
                                        be modeled with a spacer block instead.

    @variable update_interval:float     Update interval in seconds. If zero,
                                        then updated only once
    '''
    def __init__(self, bg=None, fg=None, align='right', padding=None,
                 update_interval=None):
        self._message = ''
        self._bg = bg
        self._fg = fg
        self._align = align
        self._padding = padding if padding is not None else Block.default_padding
        # blinking enabled
        self._blink = False
        # blinking state: False=normal bg, True=blink bg
        self._blinkingstate = False
        # controls blinking state toggle on and off
        self._blinkingtimer = None
        self._active = True
        self._interval = update_interval if update_interval is not None \
                                         else Block.default_update_interval
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
        if self._blinkingtimer:
            self._blinkingtimer.cancel()

    '''
    Enables/disables blinking effect: background is flashed red each blink_interval
    '''
    def set_blink(self, on):
        if self._blink != on:
            if on:
                self._create_blink_timer()
            else:
                self._blinkingstate = False
                self._blinkingtimer.cancel()
                self._blinkingtimer = None
            self._blink = on

    def _create_blink_timer(self):
        self._blinkingtimer = threading.Timer(Block.blink_interval,
                                functools.partial(Block._on_blink_timer, self))
        self._blinkingtimer.start()

    def _on_blink_timer(self):
        self._blinkingstate = not self._blinkingstate
        self._create_blink_timer()
        # TODO: optimize: only bg attribute needs to be updated here
        # therefore we don't need to run the whole thing.
        self._process()


    def _process(self):
        content = ''
        bg = Block.blink_bg if self._blinkingstate else self._bg
        if bg:
            content += '^bg(' + bg + ')'
        if self._fg:
            content += '^fg(' + self._fg + ')'
        for i in range(0, self._padding[0]):
            content += ' '

        # update() is defined in derived classes
        content += self.update()

        for i in range(0, self._padding[1]):
            content += ' '
        if bg:
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
