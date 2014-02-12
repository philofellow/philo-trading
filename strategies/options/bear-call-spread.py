#!/usr/bin/python

# this program calculates potential outcomes of selling call spread.

import os, sys, numpy

def GetPriceSamples(price, rg, num):
	min = price * (1 - rg)
	if min < 0:
		min = 0
	max = price * (1 + rg)
	step = (max - min) / num
	return numpy.arange(min, max, step)

if len(sys.argv) != 6:
	print 'USAGE:', sys.argv[0], 'stock_price call_strike_low call_price_low_bid call_strike_high call_price_high_ask'
	sys.exit()

stock_price = float(sys.argv[1])
call_strike_low = float(sys.argv[2])
call_price_low = float(sys.argv[3])

call_strike_high = float(sys.argv[4])
call_price_high = float(sys.argv[5])

range = 0.20 

credit = call_price_low - call_price_high

for p in GetPriceSamples(stock_price, range, 20):
	if p < call_strike_low:
		call_profit = credit
	if call_strike_low <= p <= call_strike_high:
		call_profit = credit - (p - call_strike_low)
	if p > call_strike_high:
		call_profit = credit - (p - call_strike_low) + (p - call_strike_high)
	
	print 'future price: %0.2f' % p, 'call profit: %0.2f' % (call_profit * 100)


