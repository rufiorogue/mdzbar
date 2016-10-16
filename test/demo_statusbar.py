#!/usr/bin/env python3

#
# mdzbar feature demonstration
#


# if the package is not located within default paths,
# add its path to the search path
import sys
sys.path.append('/home/aldn/pr/sw')


from mdzbar.bar import Bar
from mdzbar.blocks.clock import Clock
from mdzbar.blocks.statictext import StaticText
from mdzbar.blocks.separator import Separator

# create the bar
bar = Bar(bg='#333333',font='Mono-10')

# create blocks
clock = Clock(fg='blue', bg='white', padding=(2,0), fmt='%H:%M:%S')
statictext = StaticText(fg='red', bg='black', padding=(1,1), text='static text')
separator = Separator(size=10)

# pack the blocks in the bar
bar.add_block(statictext)
bar.add_block(separator)
bar.add_block(clock)

# main loop
bar.run()

print("Exited")

