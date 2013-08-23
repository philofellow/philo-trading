#!/usr/bin/python

# compute max gain, max loss and other property of an investment on a stock, when a collar is applied.
# used for hedge stock volatility, but only to persue divident

import sys, os, math, numpy

DIVIDENT_YIELD = 0.2

strike_time = 4 # months

RANGE = 0.5 # stock price at expiration will be stock_price * (1 - range ) to stock_price * (1 + range)

YEAR_ROUND = 12.0 / strike_time

def LoadOptionsFile(f, name):
	opt = open(f, 'r')
	call = dict()
	put = dict()
	for line in opt:
		if 'Nasdaq Real Time Price' in line:
			price = float(line.split()[0])
			continue
		if name in line[:5] and 'N/A' not in line:
			data = line.split()
			if 'Up' in data:
				data.remove('Up')
			if 'Down' in data:
				data.remove('Down')
			strike = float(data[7])
			call_price = (float(data[3]) + float(data[4])) / 2
			put_price = (float(data[11]) + float(data[12])) / 2
			call[strike] = call_price
			put[strike] = put_price
	return price, call, put

def GetPriceSamples(price, rg, num):
	min = price * (1 - rg)
	max = price * (1 + rg)
	step = (max - min) / num
	return numpy.arange(min, max, step)

def ComputeYield(c_strike, c_price, p_strike, p_price, price, divident):
	print "----- c_strike:", c_strike, "p_strike:", p_strike, "c_price:", c_price, "p_price:", p_price, "stock_price:", price
	cost = price - c_price + p_price 

	for p in GetPriceSamples(price, RANGE, 20):
		if p >= c_strike:
			revenue = c_strike + divident
		elif p < c_strike and p > p_strike:
			revenue = p + divident
		elif p <= p_strike:
			revenue = p_strike + divident
		else:
			print "impossible"

		annualized_yield = math.pow((1 + (revenue - cost) / cost), YEAR_ROUND) - 1
		print "future price:", p, "annualized yield:", annualized_yield


if len(sys.argv) != 1:
	print 'USAGE: ./collar.py'
	sys.exit()


price, call, put = LoadOptionsFile("agnc_201309.opt", "AGNC")
print '===== PARAMETERS ====='
print "rounds in a year:", YEAR_ROUND
divident = math.pow(1 + DIVIDENT_YIELD, 1 / YEAR_ROUND) * price - price
print "divident:", divident


print '===== YIELD TABLE ====='

for call_strike in call.keys():
	if call_strike > price:
		for put_strike in put.keys():
			if put_strike < price:
				ComputeYield(call_strike, call[call_strike], put_strike, put[put_strike], price, divident)


