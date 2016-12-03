#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#


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
        self._brief_status = ''
        self._brief_status_source = ''
        self._detailed_status = ''
        self._detailed_status_source = ''
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
        # schedule first block update ASAP
        self._timer = threading.Timer(0, \
                    functools.partial(Block._on_block_update_timer, self))
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

    def _on_block_update_timer(self):
        # calls overridden block update()
        update_result = self.update()
        if isinstance(update_result, list):
            [self._brief_status_source, self._detailed_status_source] = \
                update_result
        else:
            self._brief_status_source = update_result
            self._detailed_status_source = ''

        # if we are not done yet, reschedule the timer
        if self._active and self._interval > 0:
            self._timer = threading.Timer(self._interval, \
                          functools.partial(Block._on_block_update_timer, self))
            self._timer.start()
        # rebuild formatted block from source strings
        self._rebuild_status_strings()


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
        # rebuild formatted block from source strings
        self._rebuild_status_strings()


    '''
    Rebuilds _brief_status and _detailed_status
    from _brief_status_source and _detailed_status_source respectively
    (adds formatting and color attributes)
    '''
    def _rebuild_status_strings(self):
        content = ''
        bg = Block.blink_bg if self._blinkingstate else self._bg
        if bg:
            content += '^bg(' + bg + ')'
        if self._fg:
            content += '^fg(' + self._fg + ')'
        for i in range(0, self._padding[0]):
            content += ' '
        content += self._brief_status_source
        for i in range(0, self._padding[1]):
            content += ' '
        if bg:
            content += '^bg()'
        if self._fg:
            content += '^fg()'
        self._brief_status = content
        self.on_changed.fire()


    '''
    Get the formatted data for the block
    '''
    def get_brief_status(self):
        return self._brief_status

    def get_detailed_status(self):
        return self._detailed_status

    '''
    @return string : block content
    Overridden
    '''
    def update(self):
        pass
