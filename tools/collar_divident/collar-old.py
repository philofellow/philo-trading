#!/usr/bin/python

# compute max gain, max loss and other property of an investment on a stock, when a collar is applied.
# used for hedge stock volatility, but only to persue divident
# work for yahoo straddle view options page
# this program is obsoleted, use main.py or main2.py instead. main2.py is the updated

import sys, os, math, numpy, datetime

MONTH = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
RANGE = 0.5 # stock price at expiration will be stock_price * (1 - range ) to stock_price * (1 + range)
SAMPLE_SIZE = 40
MAX_LOSS = -0.15

def LoadOptionsFile(f):
	name = f.split('_')[0]
	opt = open(f, 'r')
	call = dict()
	put = dict()
	for line in opt:
		if 'EDT' in line:
			price = float(line.split()[0])
			continue
		if 'Options Expiring' in line:
			exp_year = int(line.split()[5])
			exp_month = MONTH[line.split()[3]]
			today = str(datetime.date.today())
			year = int(today.split('-')[0])
			month = int(today.split('-')[1])
			diff = 12 * (exp_year - year) + (exp_month - month)
			continue
		if name in line[:len(name)] and 'N/A' not in line:
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
	return diff, price, call, put

def GetPriceSamples(price, rg, num):
	min = price * (1 - rg)
	max = price * (1 + rg)
	step = (max - min) / num
	return numpy.arange(min, max, step)

def ComputeYield(c_strike, c_price, p_strike, p_price, price, divident, months):
	cost = price - c_price + p_price 
	p_to_yield = dict()
	for p in GetPriceSamples(price, RANGE, SAMPLE_SIZE):
		if p >= c_strike:
			revenue = c_strike + divident
		elif p < c_strike and p > p_strike:
			revenue = p + divident
		else:
			revenue = p_strike + divident

		annualized_yield = math.pow((1 + (revenue - cost) / cost), 12.0 / months) - 1
		if annualized_yield < MAX_LOSS:
			return None 
		p_to_yield[p] = annualized_yield		
	return p_to_yield

if len(sys.argv) != 3:
	print 'USAGE: ./collar.py file divident'
	sys.exit()

divident = float(sys.argv[2])

month_diff, price, call, put = LoadOptionsFile(sys.argv[1])
print '===== PARAMETERS ====='
print 'current stock price:', price
print "options are expired after", month_diff, 'months'
print "divident within", month_diff, 'months:', divident

print '===== YIELD TABLE ====='

for c_strike in call.keys():
	if c_strike > price:
		for p_strike in put.keys():
			if p_strike < price:
				print "----- c_strike:", c_strike, "p_strike:", p_strike, "c_price:", call[c_strike], "p_price:", put[p_strike]
				yield_table = ComputeYield(c_strike, call[c_strike], p_strike, put[p_strike], price, divident, month_diff)
				if yield_table is None:
					print 'exceeds max loss, drop'
				else:					
					for p in sorted(yield_table.keys()):
						print "future price:", p, "annualized yield:", yield_table[p]

