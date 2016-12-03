#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#

import subprocess
import shlex
import asyncio
import signal
import functools
import mdzbar.utils as utils

__all__ = ['Bar']


class Bar:
    def __init__(self,
                font='Monospace',
                bg='#000000',
                fg='#ffffff',
                length=0,
                size=20,
                edge='top',
                edge_offset=0,
                content_align='right'):
        self._font = font
        self._bg_color = bg
        self._fg_color = fg
        self._content_align = content_align
        self._calculate_bar_geometry(edge,edge_offset,length,size)
        self._blocks = []
        self._loop = asyncio.get_event_loop()

    '''
    Calculates bar's position and dimensions from
    edge, offset, length and size
    '''
    def _calculate_bar_geometry(self, edge, edge_offset, length, size):
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
        cmd = 'dzen2 -fn %s -bg %s -fg %s -x %d -y %d -w %d -h %d -ta %s' %(
                self._font,
                self._bg_color,
                self._fg_color,
                self._x,
                self._y,
                self._w,
                self._h,
                self._content_align[0])
        args = shlex.split(cmd)

        print('Running: ' + ' '.join(args))
        # execute child process
        self._backend = subprocess.Popen(args,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE)

        # setup reader
        self._loop.add_reader(self._backend.stdout,
                              functools.partial(Bar._cb_read, self))

        # setup signal handlers
        for signame in ('SIGINT', 'SIGTERM'):
            self._loop.add_signal_handler(
                    getattr(signal, signame),
                    functools.partial(Bar._cb_terminate, self, signame))

        # activate all blocks
        self._loop.call_soon(functools.partial(Bar._cb_activate_all, self))

        print('Event loop started!')
        try:
            self._loop.run_forever()
        finally:
            print('Handled even loop exception')
            self._cb_deactivate_all()
            self._loop.close()


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
        block_content_list = [x.get_brief_status() for x in self._blocks]
        merged = ''.join(block_content_list)
        merged += '\n'
        print("dzen string : "+ merged)
        f = self._backend.stdin
        f.write(bytes(merged,'UTF-8'))
        f.flush()

    def _cb_read(self):
        # print('cb_read')
        buffer = self._backend.stdout.read()
        # print(buffer)

    '''
    Callback which is called when application receives SIGTERM or SIGINT
    '''
    def _cb_terminate(self, signame):
        print("Got signal %s: exit" % signame)
        self._backend.terminate()
        self._loop.stop()



