#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#


from ..block import Block
import mdzbar.utils as utils

__all__ = ['Battery']

# characters from FontAwesome
CHR_BAT_0    = chr(0xf244)
CHR_BAT_25   = chr(0xf243)
CHR_BAT_50   = chr(0xf242)
CHR_BAT_75   = chr(0xf241)
CHR_BAT_100  = chr(0xf240)
CHR_CHARGING = chr(0xf0e7)

'''
 returns dict with keys:
 level   = 0..1
 mode    = 'Full', 'Charging', 'Discharging'
 time    = hours left to fully charge if mode = 'Charging',
                      to fully discharge if mode = 'Discharging',
           or 0 otherwise
'''
def read_battery_info():
    sys_file = '/sys/class/power_supply/BAT1/uevent'
    result = {}
    kv = utils.parse_keyval_file(sys_file)
    # power in Watts
    current =  kv['POWER_SUPPLY_CURRENT_NOW'] * 1e-6
    # charge in Amper*hours
    charge_now = kv['POWER_SUPPLY_CHARGE_NOW'] * 1e-6
    charge_full = kv['POWER_SUPPLY_CHARGE_FULL'] * 1e-6
    result['level'] = charge_now/charge_full 
    result['mode'] = kv['POWER_SUPPLY_STATUS']
    if result['mode'] == 'Charging':
        result['time'] = (charge_full - charge_now) / current
    elif result['mode'] == 'Discharging':
        result['time'] = charge_now / current
    else:
        result['time'] = 0

    return result


def select_battery_icon(level):
    if level <= 0.1:
        return CHR_BAT_0
    elif level <= 0.25:
        return CHR_BAT_25
    elif level <= 0.5:
        return CHR_BAT_50
    elif level <= 0.75:
        return CHR_BAT_75
    else:
        return CHR_BAT_100

class Battery(Block):
    def __init__(self,  *args, **kwargs):
        Block.__init__(self, update_interval=10, *args, **kwargs)

    def update(self):
        print('Battery.update')
        battery_info = read_battery_info()
        is_charging = battery_info['mode'] == 'Charging'
        is_discharging = battery_info['mode'] == 'Discharging'
        level = battery_info['level']
        time = battery_info['time']
        brief_status = '^fn(FontAwesome)' 
        if is_charging:
            brief_status += '^fg(green)'
            brief_status += CHR_CHARGING + ' '
        brief_status += select_battery_icon(level)
        brief_status += '^fn()^fg()'
        if (not is_charging) and (not is_discharging):
            detailed_status = battery_info['mode']
        else:
            detailed_status = '%s, %d%%, %s left' % (
                                battery_info['mode'],
                                int(battery_info['level'] * 100),
                                utils.seconds_to_hms(battery_info['time']*3600))
        self.set_blink(is_discharging and level <= 0.1)
        return brief_status + detailed_status

