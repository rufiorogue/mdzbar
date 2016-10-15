#!/usr/bin/env python3

import asyncio

'''
Event Hook by Michael Foord:
http://www.voidspace.org.uk/python/weblog/arch_d7_2007_02_03.shtml#e616
'''
class EventHook(object):
    def __init__(self):
        self._handlers = []
        self._loop = asyncio.get_event_loop()

    def __iadd__(self, handler):
        self._handlers.append(handler)
        return self

    def __isub__(self, handler):
        self._handlers.remove(handler)
        return self

    def fire(self, *args):
        for handler in self._handlers:
            # handler(*args, **keywargs)
            if self._loop.is_running():
                self._loop.call_soon_threadsafe(handler,args)

    def clearObjectHandlers(self, inObject):
        for theHandler in self._handlers:
            if theHandler.im_self == inObject:
                self -= theHandler
