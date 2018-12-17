#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import datetime as dt
import matplotlib.pyplot as plt
import myiwlist


cells = myiwlist.scan()
cells = myiwlist.parse(cells)
nets = [C.essid for C in cells]

Ys = [[] for _ in nets]
X,Y2g,Y5g = [],[],[]
while not os.path.isfile('STOP'):
   cells = myiwlist.scan()
   cells = myiwlist.parse(cells)
   nets = [C.essid for C in cells]

   now = dt.datetime.now()
   print(now)
   X.append(now)
   for C in cells:
      ind = nets.index(C.essid)
      Ys[ind].append(C.signal_level_dBm)
      if C.essid == '430 b forest home': Y2g.append(C.signal_level_dBm)
      elif C.essid == '430 b forest home-5G': Y5g.append(C.signal_level_dBm)

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
for i in range(len(Ys)):
   y = Ys[i]
   l = nets[i]
   ax.plot(X,y,label=l)
#ax.plot(X, Y2g)
#ax.plot(X, Y5g)
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
