#!/usr/bin/env python3

__all__ = ['Bar']

import subprocess
import threading
import asyncio
import signal
import functools
import mdzbar.utils as utils


class Bar:
    def __init__(self, font='Terminus', bg='#000000', fg='#ffffff',
                length=0, size=24, edge='top', edge_offset=0):
        self._font = font
        self._bg_color = bg
        self._fg_color = fg

        (sw,sh) = utils.get_screen_size()
        if edge == 'top':
            x = 0
            y = edge_offset
            w = length if length > 0 else sw
            h = size
        elif edge == 'bottom':
            x = 0
            y = sh - edge_offset
            w = length if length > 0 else sw
            h = size
        elif edge == 'left':
            x = edge_offset
            y = 0
            w = size
            h = length if length > 0 else sh
        elif edge == 'right':
            x = sw - edge_offset
            y = 0
            w = size
            h = length if length > 0 else sh
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._blocks = []

    '''
    Adds the block to the bar
    '''
    def add_block(self, block):
        self._blocks.append(block)
        block.on_changed += functools.partial(Bar._cb_changed,self)

    '''
    Remove the block from the bar
    '''
    def remove_block(self, block):
        self._blocks.remove(block)

    '''
    Creates backend process and starts the event loop
    which handles events from the backend, the blocks and operating system
    '''
    def run(self):
        args = [
                'dzen2',
                '-fn', self._font,
                '-bg', self._bg_color,
                '-fg', self._fg_color,
                #'-l', str(1), #lines
                '-x', str(self._x),
                '-y', str(self._y),
                '-w', str(self._w),
                '-h', str(self._h),
                ]
        args = ['cat', '>', 'f']
        print('Running: ' + ' '.join(args))
        # execute child process
        self._backend = subprocess.Popen(args,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         universal_newlines=True,
                                         shell=True)

        loop = asyncio.get_event_loop()
        # setup reader
        loop.add_reader(self._backend.stdout, functools.partial(Bar._cb_read, self))

        # setup signal handlers
        self._evloop = loop
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(
                    getattr (signal, signame),
                    functools.partial(Bar._cb_terminate, self, signame))

        # activate all blocks
        loop.call_soon(functools.partial(Bar._cb_activate_all, self))

        print('Event loop started!')
        try:
            loop.run_forever()
        finally:
            self._cb_deactivate_all()
            loop.close()


    def _cb_activate_all(self):
        for i in self._blocks:
            i.activate()

    def _cb_deactivate_all(self):
        for i in self._blocks:
            i.deactivate()

    '''
    Callback which is called when any block data is changed
    and therfore the bar needs to be updated
    '''
    def _cb_changed(self, *args):
        print("Triggered changed event")
        # create a long string from data of all blocks merged into one
        block_content_list = [str(x) for x in self._blocks]
        merged = ''.join(block_content_list)
        merged += '\n'
        print("dzen string : "+ merged)
        self._backend.stdin.write(merged)

    def _cb_read(self):
        print('cb_read')
        buffer = self._backend.stdout.read()
        print(buffer)

    '''
    Callback which is called when application receives SIGTERM or SIGINT
    '''
    def _cb_terminate(self, signame):
        print("Got signal %s: exit" % signame)
        self._backend.terminate()
        self._evloop.stop()



