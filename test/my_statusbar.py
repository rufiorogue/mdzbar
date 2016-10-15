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

# create the bar
bar = Bar(bg='red')

# create blocks
clock = Clock()

# pack the blocks in the bar
bar.add_block(clock)

# main loop
bar.run()

print("Exited")

