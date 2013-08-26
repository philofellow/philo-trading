#!/usr/bin/python

# compute max gain, max loss and other property of an investment on a stock, when a collar is applied.
# used for hedge stock volatility, but only to persue divident

import sys, os, math, numpy, datetime, urllib2

STOCKS_FILE = 'divident.data'
MONTH = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
RANGE = 0.5 # stock price at expiration will be stock_price * (1 - range ) to stock_price * (1 + range)
SAMPLE_SIZE = 40
MAX_LOSS = -0.15

class Stock:
	def __init__(self, price, divident, ex_div_month, ex_div_date, pay_month, pay_date):
		self.price = float(price)
		self.divident = float(divident)
		self.quarter_divident = self.divident / 4.0
		self.ex_div_year = int(str(datetime.date.today()).split('-')[0])
		self.ex_div_month = int(ex_div_month)
		self.ex_div_date = int(ex_div_date)
		if self.ex_div_month > 9:
			self.next_ex_div_year = self.ex_div_year + 1
		else:
			self.next_ex_div_year = self.ex_div_year
		if self.ex_div_month == 9:
			self.next_ex_div_month = 12
		else:
			self.next_ex_div_month = (self.ex_div_month + 3) % 12
		self.next_ex_div_date = self.ex_div_date
		self.pay_month = int(pay_month)
		self.pay_date = int(pay_date)
	
	def Print(self):
		print 'price ' + str(self.price) + ', quarter_divident ' + str(self.quarter_divident) + ', ex_div_date ' \
				+ str(self.ex_div_year) + '/' + str(self.ex_div_month) + '/' + str(self.ex_div_date) \
				+ ', next_ex_div_date ' + str(self.next_ex_div_year) + '/' + str(self.next_ex_div_month) \
				+ '/' + str(self.next_ex_div_date) 

class StockMap:

        # {symbol:StockEntry}, index starts from 0, date and index increase correspondingly 
        stock_map = dict()
	stock_file = 'divident.data'
        # load stock data from file
        def __init__(self):
		f = open(self.stock_file, 'r')
		f.readline() # skip first line
		for line in f:
			if 'N/A' in line:
				continue
			data = line.split()
			symbol = data[0]
			self.stock_map[data[0]] = Stock(data[-4], data[-3], data[-2].split('/')[0], \
					data[-2].split('/')[1], data[-1].split('/')[0], data[-1].split('/')[1])

	def Print(self):
		for symbol in self.stock_map.keys():
			print 'symbol: ', symbol
			self.stock_map[symbol].Print()

def GetNextMonth(month, year):
	if month == 12:
		return 1, year + 1
	else:
		return month + 1, year

def IsEmptyOptionFile(csv, symbol):
	f = open(csv, 'r')
	data = f.read()
	return not symbol in data

def GetValue(val):
	if 'NaN' in val:
		return 0.0
	else:
		return float(val)

def LoadOptionFile(f, symbol):
	opt = open(f, 'r')
	call = dict()
	put = dict()
	opt.readline()
	for line in opt:
		if 'C,' in line:
			data = line.split(',')
			strike = GetValue(data[2])
			call_price = (GetValue(data[6])) # use bid price since selling call
			call[strike] = call_price
		
		elif 'P,' in line:
			data = line.split(',')
			strike = GetValue(data[2])
			put_price = (GetValue(data[7])) # use ask price since buying call
			put[strike] = put_price
	return call, put

def DownloadBestOption(symbol, m, y):
	month, year = GetNextMonth(m, y)
	csv = DownloadOption(symbol, month, year)
	for i in range(3): # take the options expiring at most 3 month later than the ex_div_date
		if IsEmptyOptionFile(csv, symbol):
			print 'empty option file:', csv
			os.system('rm ' + csv)
			month, year = GetNextMonth(month, year)
			csv = DownloadOption(symbol, month, year)
		else:
			break
	if IsEmptyOptionFile(csv, symbol):
		return ''
	return csv
			

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


def DownloadOption(symbol, month, year):

	link = 'http://www.optionpain.altervista.org/csv.php?symbol=' \
			+ symbol + '&month=' + str(month) + '&year=' + str(year)

	print 'download <' + symbol + '> from ' + link
	csv = urllib2.urlopen(link).read()
	path = symbol + '_' + str(year) + '_' + str(month) + '.csv'
	f = open(path, 'w')
    	f.write(csv)
	return path

def GetMonthDiff(later_month, later_year, earlier_month, earlier_year):
	diff = 0	
	while earlier_month != later_month or earlier_year != later_year:
		earlier_month, earlier_year = GetNextMonth(earlier_month, earlier_year)
		diff += 1
	return diff

if len(sys.argv) != 1:
	print 'USAGE: ./main.py'
	sys.exit()

os.system('rm *.csv')

div_data = StockMap()

for symbol in div_data.stock_map.keys():
	price = div_data.stock_map[symbol].price
	divident = div_data.stock_map[symbol].quarter_divident

	print '\n\n===== PARAMETERS ====='
	print 'stock:', symbol
	print 'current stock price:', price
	div_data.stock_map[symbol].Print()
	
	csv = DownloadBestOption(symbol, div_data.stock_map[symbol].next_ex_div_month, div_data.stock_map[symbol].next_ex_div_year)
	if csv == '':
		print 'not appropriate options for', symbol, 'pass the analysis'	
		continue
	print 'option file:', csv

	opt_month = int(csv.split('_')[2][:-4])
	opt_year = int(csv.split('_')[1])	
	now_month = int(str(datetime.date.today()).split('-')[1])
	now_year = int(str(datetime.date.today()).split('-')[0])
	month_diff = GetMonthDiff(opt_month, opt_year, now_month, now_year)
	print "options are expired after", month_diff, 'months'
	print "divident within date " + str(now_year) + '/' + str(now_month) + ' to ' + str(opt_year) + '/' + str(opt_month) + ' is ' + str(divident)

	call, put = LoadOptionFile(csv, symbol)	
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
