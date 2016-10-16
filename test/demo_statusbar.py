#!/usr/bin/env python3
#
# mdzbar: Modular statusbar using dzen2 as backend
#
# Copyright (C) 2016 Oleksandr Dunayevskyy
# See LICENSE file for license details.
#


#
# mdzbar feature demonstration
#


# if the package is not located within default paths,
# add its path to the search path
import sys
sys.path.append('/home/aldn/pr/sw')


from mdzbar.bar import Bar
from mdzbar.block import Block
from mdzbar.blocks.clock import Clock
from mdzbar.blocks.statictext import StaticText
from mdzbar.blocks.separator import Separator

#
# create the bar
#
bar = Bar(bg='#333333',font='Terminus-10')

#
# create blocks
#

Block.default_padding = (1,1)
Block.default_update_interval = 3

clock = Clock(fg='cyan', bg='black', padding=(2,0), fmt='%H:%M:%S')

text = StaticText(bg='white', fg='#222222', text='hello!')

blinking_text = StaticText(fg='white', text='blinking')
blinking_text.set_blink(True)

separator = Separator(size=20)

#
# pack the blocks in the bar
#
bar.add_block(blinking_text)
bar.add_block(text)
bar.add_block(separator)
bar.add_block(clock)


# main loop
bar.run()


print("Exited")

