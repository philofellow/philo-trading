#!/usr/bin/python

# compute put / price for a list of stocks for future several months
#! /usr/bin/python

import sys
sys.path.append('../../')
import time, os, ptConst, math, numpy, datetime, urllib2, random

MONTH = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
SYMBOL_LIST = 'symbols.data'

class Date:
	valid = True
	def __init__(self, date_str): # mm/dd/yyyy
		if '-' in date_str:
			date_str = '0/0/0'
		date = date_str.split('/')
		self.year = int(date[2])
		self.month = int(date[0])
		self.day = int(date[1])
		if date_str == '0/0/0':
			self.valid = False	
	def GetString(self):
		return '%02d/%02d/%04d' % (self.month, self.day, self.year)
	
	def __lt__(self, other):
		me = "%04d%02d%02d" % (self.year, self.month, self.day)
		it = "%04d%02d%02d" % (other.year, other.month, other.day)
		return me < it
	def __eq__(self, other):
		me = "%04d%02d%02d" % (self.year, self.month, self.day)
		it = "%04d%02d%02d" % (other.year, other.month, other.day)
		return me == it
	def MoveToNextMonth(self):
		if self.month == 12:
			self.month = 1
			self.year = self.year + 1
		else:
			self.month += 1
	def Print(self):
		print ('%02d/%02d/%04d' % (self.month, self.day, self.year))

	@staticmethod
	def GetNow():
		now_month = int(str(datetime.date.today()).split('-')[1])
		now_day = int(str(datetime.date.today()).split('-')[2])
		now_year = int(str(datetime.date.today()).split('-')[0])
		return Date('%02s/%02s/%04s' % (now_month, now_day, now_year))

class Stock:
	valid = True
	def __init__(self, price):
		self.price = float(price)
		if self.price == '0.0':
			self.valid = False	
			ptConst.logging.warning('parameter not valid') 
	def Print(self):
		print 'price ' + str(self.price)

class StockMap:

        # {symbol:StockEntry}, index starts from 0, date and index increase correspondingly 
        stock_map = dict()
	valid = True
        # load stock data from file
        def __init__(self):
		f = open(SYMBOL_LIST, 'r')
		ptConst.logging.info('initilizing stock map from file ' + SYMBOL_LIST)
		for line in f:
			data = line.split()[-1].split(',')
			symbol = data[1][1:-1]
			price = float(data[2])
			self.stock_map[symbol] = Stock(price)
			ptConst.logging.info('adding ' + symbol + ' to stock map')

	def Print(self):
		for symbol in self.stock_map.keys():
			print 'symbol: ', symbol
			self.stock_map[symbol].Print()

def GetDateFromString(date_str):
	date = date_str.split('-')
	if date[0] not in MONTH.keys():
		return '0/0/0'
	if date[1] == '': return '0/0/0'
	if date[2] == '': return '0/0/0'
	return str(MONTH[date[0]]) + '/' + date[1] + '/' + date[2]

def IsEmptyOptionFile(opt, symbol):
	f = open(opt, 'r')
	data = f.read()
	return not symbol in data

def GetValue(val):
	if 'NaN' in val:
		return 0.0
	else:
		return float(val)

def LoadOptionFile(f, symbol):
	ptConst.logging.info('loading options file ' + f)
	opt = open(f, 'r')
	call = dict()
	put = dict()
	print opt.readline()
	for line in opt:
		print line
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

def GetOptionExpireDate(opt):
	f = open(opt, 'r')
	f.readline()
	line = f.readline()
	time = line.split(',')[0][-15:-9]
	year = '20' + time[0:2]
	month = time[2:4]
	day = time[4:]
	f.close()
	return Date(month + '/' + day + '/' + year)

def LoadOptions(symbol, date):
	tmp_date = date
	options_map = dict()
	for i in range(6): # take the options expiring at most 6 month later
		opt = DownloadOption(symbol, tmp_date.month, tmp_date.year)
		if IsEmptyOptionFile(opt, symbol):
		#	print 'empty option file:', opt
			os.system('rm ' + opt)
			tmp_date.MoveToNextMonth()
			ptConst.logging.info('option file ' + opt + ' is empty, move to next month')
			continue
		call, put = LoadOptionFile(opt, symbol)
		options_map[tmp_date.GetString()] = (call, put)
		os.system('rm ' + opt)
		tmp_date.MoveToNextMonth()
	return options_map
	
def DownloadOption(symbol, month, year):

	link = 'http://www.optionpain.altervista.org/csv.php?symbol=' \
			+ symbol + '&month=' + str(month) + '&year=' + str(year)

	ptConst.logging.info('download options of <' + symbol + '> from ' + link)
	opt = urllib2.urlopen(link).read()
	path = symbol + '_' + str(year) + '_' + str(month) + '.opt'
	f = open(path, 'w')
    	f.write(opt)
	return path


if len(sys.argv) != 1:
	print 'USAGE: ', argv[0]
	sys.exit()

ptConst.logging.info('===== Start a new run of Divident-Collar-Analysis =====')

os.system('rm -f *.opt')
os.system('./stock_quota.sh')

stocks = StockMap()
stocks.Print()

for symbol in stocks.stock_map.keys():
	price = stocks.stock_map[symbol].price
	ptConst.logging.info('=== begin analysis for ' + symbol + ', price: ' + str(price))
	stock = stocks.stock_map[symbol]
	opt_map = LoadOptions(symbol, Date.GetNow())
	if len(opt_map.keys()) == 0:
		print 'no appropriate options for', symbol, 'pass'	
		continue
	print opt_map


'''

	opt_month = int(opt.split('_')[2][:-4])
	opt_year = int(opt.split('_')[1])	
	now_month = int(str(datetime.date.today()).split('-')[1])
	now_year = int(str(datetime.date.today()).split('-')[0])
	month_diff = GetMonthDiff(opt_month, opt_year, now_month, now_year)
	print 'options are expired at', GetOptionExpireDate(opt).GetString(), 'which is', month_diff, 'months later'
	print 'dividend within date ' + str(now_year) + '/' + str(now_month) + ' to ' + str(opt_year) + '/' + str(opt_month) + ' is ' + str(dividend)
	ptConst.logging.info('options are expired at ' + GetOptionExpireDate(opt).GetString())
	ptConst.logging.info('dividend within date ' + str(now_year) + '/' + str(now_month) \
			+ ' to ' + str(opt_year) + '/' + str(opt_month) + ' is ' + str(dividend))
	
	shares = GetShares(price)
	if shares == 0:
		ptConst.logging.info('$' + str(CASH) + ' is not enough to buy 100 shares, pass')
		print '$' + str(CASH) + ' is not enough to buy 100 shares, pass'
		continue
	ptConst.logging.info('can buy ' + str(shares * 100) + ' shares with $' + str(CASH))
	ptConst.logging.info('every cent less converts to ' + str(shares) + ' dollars')
	print 'can buy ' + str(shares * 100) + ' with $' + str(CASH)

	call, put = LoadOptionFile(opt, symbol)	

	print '===== YIELD TABLE ====='
	ptConst.logging.info('begin generating yield table')
	for c_strike in call.keys():
		if c_strike > price:
			for p_strike in put.keys():
				if p_strike < c_strike:
					print '----- c_strike:', c_strike, 'p_strike:', p_strike, 'c_price:', call[c_strike], 'p_price:', put[p_strike]
					yield_table = ComputeYield(c_strike, call[c_strike], p_strike, put[p_strike], price, dividend, month_diff, shares)
					if yield_table is None:
						print 'exceeds max loss drop'
					else:	
						table = sorted(yield_table.keys())				
						for p in table:
							if yield_table[p][0] > 0:
								print 'break even price: ' + str(p)
								break
						print ' max loss: ' + str(yield_table[table[0]][0]) \
								+ ', term yield: ' + str(yield_table[table[0]][1]) \
								+ ', annualized yield: ' + str(yield_table[table[0]][2])
'''
