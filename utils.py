#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#


# import xcb
# import os
import asyncio

def get_screen_size():
    #conn = xcb.connect(display=os.environ['DISPLAY'], fd=3, auth='NAME:binary-data')
    return (1920, 1080)

def parse_keyval_file(path):
    raw_values = {}
    with open(path) as f:
        for var in f.read().splitlines():
            k, v = var.split("=")
            try:
                raw_values[k] = int(v)
            except ValueError:
                raw_values[k] = v
    return raw_values


def hms_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 3600 * h + 60 * m + s

def seconds_to_hms(secs):
    m, s = divmod(secs, 60)
    h, m = divmod(m, 60)
    return '%d:%02d:%02d' % (h, m, s)
