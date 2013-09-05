#!/usr/bin/python

# this program compares the profit and loss of buying stock and buying call.

import os, sys, numpy

def GetPriceSamples(price, rg, num):
	min = price * (1 - rg)
	if min < 0:
		min = 0
	max = price * (1 + rg)
	step = (max - min) / num
	return numpy.arange(min, max, step)

stock_price = 14.3
call_strike = 17
call_price = 1.08
contract_num = 2
stock_num = 100
range = 3 

stock_cost = stock_price * stock_num
call_cost = call_price * contract_num * 100

print 'if buy stock, cost:', stock_cost
print 'if buy call, cost:', call_cost
for p in GetPriceSamples(stock_price, range, 20):
	if p < call_strike:
		call_profit = -call_cost
	if p >= call_strike:
		call_profit = (p - call_strike) * contract_num * 100 - call_cost
	stock_profit = p * stock_num - stock_cost
	print 'future price:', p, 'stock profit:', stock_profit, 'yield:', stock_profit/stock_cost, 'call profit:', call_profit, 'yield:', call_profit/call_cost


