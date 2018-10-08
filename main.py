#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import myiwlist

cells = myiwlist.scan()
cells = myiwlist.parse(cells)
for C in cells:
   print(C)
   print('')
