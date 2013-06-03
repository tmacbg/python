#!/usr/bin/python

from matplotlib.dates import strpdate2num, epoch2num
import numpy as np
from pylab import figure, show, cm

datefmt = "%a %b %d %H:%M:%S CEST %Y"
datafile = "cpu.dat"

def parsedate(x):
    global datefmt
    try:
        res = epoch2num( int(x) )
    except:
        try:
            res = strpdate2num(datefmt)(x)
        except:
            print("Cannot parse date ('"+x+"')")
            exit(1)
    return res

# parse data file
t,a,b,c = np.loadtxt(
    datafile, delimiter=';',
    converters={0:parsedate},
    unpack=True)

fig = figure()
ax = fig.add_axes((0.1,0.1,0.7,0.85))
# limit y axis to 0
ax.set_ylim(0);

# colors
colors=['b','g','r']
fill=[(0.5,0.5,1), (0.5,1,0.5), (1,0.5,0.5)]

# plot
for x in [c,b,a]:
    ax.plot_date(t, x, '-', lw=2, color=colors.pop())
    ax.fill_between(t, x, color=fill.pop())

# legend
ax.legend(['max','avg','min'], loc=(1.03,0.4), frameon=False)

fig.autofmt_xdate()
show()
