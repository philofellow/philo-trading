#!/usr/bin/python

import sys, os

f = open('divident.data', 'r')
f1 = open('symbols.data', 'w')

for line in f:
	symbol = line.split()[0]
	f1.write(symbol + ' ')

