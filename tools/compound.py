#!/usr/bin/python

import sys,os

if len(sys.argv) != 4:
	print 'USAGE: ./compound.py yearly_invest year rate'
	sys.exit()

rate = float(sys.argv[3]) 
year = int(sys.argv[2])
yearly_invest = float(sys.argv[1])

end = 0

for i in range(year):
	begin = end + yearly_invest
	end = begin * (1 + rate)

print end
