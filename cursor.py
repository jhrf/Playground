#!/usr/bin/env python
import curses
import time
import sys
from blessings import Terminal

term = Terminal()
with term.location(0, term.height - 1):
    print 'Here is the bottom.'
print 'This is back where I came from.'

with term.location(0,term.height- 3):
    print 'Tits on cheese etc.'