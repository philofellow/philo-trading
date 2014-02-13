#!/usr/bin/python

# obtain the call/put price for a high dividend stock/bdc/reit
# if out-the-money call price is high, then buy the stock and sell the call
# if out-the-money put price is high, then sell the put and take the premium or get the stock if being put 

#! /usr/bin/python

import sys
sys.path.append('../../')
import time, os, ptConst, math, numpy, datetime, urllib2, random

MONTH = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
SYMBOL_LIST = 'symbols.data'
CASH = 2000.0
STOCK_TRADING_FEE = 3.95

class Date:
	valid = True
	def __init__(self): # init to today
		today = str(datetime.date.today())
		self.year = int(today.split('-')[0])
		self.month = int(today.split('-')[1])
		self.day = int(today.split('-')[2])

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
		return str(self.month) + '/' + str(self.day) + '/' + str(self.year)
	
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

class Stock:
	valid = True
	def __init__(self, price, dividend, ex_date, decl_date):
		self.price = float(price)
		self.dividend = float(dividend)
		self.ex_date = Date(ex_date)
		self.decl_date = Date(decl_date)
		if self.price == '0.0' or not self.ex_date.valid or not self.decl_date.valid:
			self.valid = False	
			ptConst.logging.warning('parameter not valid') 
	def Print(self):
		print 'price ' + str(self.price) + ', dividend ' + str(self.dividend) \
				+ ', decl_date ' + self.decl_date.GetString() \
				+ ', ex_date ' + self.ex_date.GetString()

class StockMap:

        # {symbol:StockEntry}, index starts from 0, date and index increase correspondingly 
        stock_map = dict()
	valid = True
        # load stock data from file
        def __init__(self):
		f = open(SYMBOL_LIST, 'r')
		ptConst.logging.info('initilizing stock map from file ' + SYMBOL_LIST)
		for line in f:
			data = line.split()
			for symbol in data:
				ptConst.logging.info('adding ' + symbol + ' to stock map')
				#self.LoadDividendDataDividendInvestor(symbol)
				self.LoadDividendDataStreetInsider(symbol)

	def Print(self):
		for symbol in self.stock_map.keys():
			print 'symbol: ', symbol
			self.stock_map[symbol].Print()

	def LoadDividendDataDividendInvestor(self, symbol):
		time.sleep(random.randint(2, 5))
		link = 'http://www.dividendinvestor.com/dividendhistory.php?symbol=' + symbol
		filename = symbol + '.div'
		data = urllib2.urlopen(link).read()
		f = open(filename, 'w')
    		f.write(data)
		f.close()
		price = '0.0'
		dividend = '0.0'
		ex_date = '0/0/0'
		decl_date = '0/0/0'
		f = open(filename, 'r')
		while True:
			line = f.readline()
			if line == '': break
			if 'Dividend Declaration Date: </td>' in line:
				line = f.readline()
				decl_date_str = f.readline().strip().split()[0]
				decl_date = GetDateFromString(decl_date_str)
			if 'Dividend Ex Date: </td>' in line:
				line = f.readline()
				ex_date_str = f.readline().strip().split()[0]
				ex_date = GetDateFromString(ex_date_str)
			if 'Dividend Amount Current:</td>' in line:
				line = f.readline()
				line = f.readline()
				dividend = self.LoadProperty(line, '$', '</b>').strip()
			if 'Latest Close Price: </td>' in line:
				line = f.readline()
				price = f.readline().strip().split()[0]


		ptConst.logging.info('parameters loaded: price = ' + price + ', dividend = ' \
				+ dividend + ', decl_date = ' + decl_date + ', ex_date = ' + ex_date)
		self.stock_map[symbol] = Stock(price, dividend, ex_date, decl_date)
	#	os.system('rm ' + filename)
	


	def LoadDividendDataStreetInsider(self, symbol):
		link = 'http://www.streetinsider.com/dividend_history.php?q=' + symbol
		filename = symbol + '.div'
		data = urllib2.urlopen(link).read()
		f = open(filename, 'w')
    		f.write(data)
		f.close()
		#os.system('wget ' + link + ' -O ' + filename)
		time.sleep(random.randint(1, 3))
		price = '0.0'
		dividend = '0.0'
		ex_date = '0/0/0'
		decl_date = '0/0/0'
		f = open(filename, 'r')
		while True:
			line = f.readline()
			if line == '': break
			if '<strong>Price:</strong>' in line:
				price = self.LoadProperty(line, '<strong>Price:</strong> ', '&nbsp; |')
				if 'N/A' in price: price = '0.0'
				if price == '': price = '0.0'
			if '<tr class="LiteHover">' in line:
				line = f.readline()
				ex_date = self.LoadProperty(line, '<td>', '<')
				if 'N/A' in ex_date: ex_date = '0/0/0'
				line = f.readline()
				dividend = self.LoadProperty(line, '<td>', '<')[1:]
				if 'N/A' in dividend: dividend = '0.0'
				f.readline()
				f.readline()
				f.readline()
				line = f.readline()
				decl_date = self.LoadProperty(line, '<td>', '<')
				if 'N/A' in decl_date: decl_date = '0/0/0'
				break
		ptConst.logging.info('parameters loaded: price = ' + price + ', dividend = ' \
				+ dividend + ', decl_date = ' + decl_date + ', ex_date = ' + ex_date)
		self.stock_map[symbol] = Stock(price, dividend, ex_date, decl_date)
	#	os.system('rm ' + filename)
		f.close()	

	def LoadDividendDataNasdaq(self, symbol):
		ex_date_mark = 'quotes_content_left_dividendhistoryGrid_exdate_0">'
		price_mark = 'qwidget_lastsale'
		div_mark = 'quotes_content_left_dividendhistoryGrid_CashAmount_0">'
		decl_date_mark = 'quotes_content_left_dividendhistoryGrid_DeclDate_0">'

		link = 'http://www.nasdaq.com/symbol/' + symbol + '/dividend-history'
		filename = symbol + '.div'
		os.system('wget ' + link + ' -O ' + filename)
		price = '0.0'
		dividend = '0.0'
		ex_date = '0/0/0'
		decl_date = '0/0/0'
		f = open(filename, 'r')
		for line in f:
			if price_mark in line:
				price = self.LoadProperty(line, '$', '<') 
			if ex_date_mark in line:
				ex_date = self.LoadProperty(line, ex_date_mark, '<') 
			if div_mark in line:
				dividend = self.LoadProperty(line, div_mark, '<') 
			if decl_date_mark in line:
				decl_date = self.LoadProperty(line, decl_date_mark, '<') 
		ptConst.logging.info('parameters loaded: price = ' + price + ', dividend = ' \
				+ dividend + ', decl_date = ' + decl_date + ', ex_date = ' + ex_date)
		self.stock_map[symbol] = Stock(price, dividend, ex_date, decl_date)
	#	os.system('rm ' + filename)
				
	def LoadProperty(self, line, begin_mark, end_mark):
		begin = line.find(begin_mark) + len(begin_mark)
		end = line[begin:].find(end_mark)
		return line[begin:][:end]

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

def OptionExpireLaterThanDate(opt, date):
	exp_date = GetOptionExpireDate(opt)
	return not (exp_date < date or exp_date == date)

def DownloadOptionAfterMonth(symbol, month):
	tmp_date = Date()
	for i in range(month): 
		tmp_date.MoveToNextMonth()
	for i in range(3): # take the options expiring at most 3 month later 
		opt = DownloadOption(symbol, tmp_date.month, tmp_date.year)
		if IsEmptyOptionFile(opt, symbol):
		#	print 'empty option file:', opt
			os.system('rm ' + opt)
			tmp_date.MoveToNextMonth()
			ptConst.logging.info('option file ' + opt + ' is empty, move to next month')
			continue
		ptConst.logging.info('find valid option file ' + opt) 
		return opt
	
	ptConst.logging.info('no valid option file') 
	return ''

def GetShares(p):
	# return max hundreds of shares with CASH
	num = 1
	while True:
		if num * 100.0 * p > CASH:
			return num - 1
		num += 1	

def GetFee(contracts_num):
	if contracts_num <= 5:
		return STOCK_TRADING_FEE + (5 * 2) 
	else: 
		return STOCK_TRADING_FEE + (8.5 + 0.15 * contracts_num) * 2

def DownloadOption(symbol, month, year):

	link = 'http://www.optionpain.altervista.org/csv.php?symbol=' \
			+ symbol + '&month=' + str(month) + '&year=' + str(year)

	ptConst.logging.info('download options of <' + symbol + '> from ' + link)
	opt = urllib2.urlopen(link).read()
	path = symbol + '_' + str(year) + '_' + str(month) + '.opt'
	f = open(path, 'w')
    	f.write(opt)
	return path

def GetNextMonth(month, year):
	if month == 12:
		return 1, year + 1
	else:
		return month + 1, year


def GetMonthDiff(later_month, later_year, earlier_month, earlier_year):
	diff = 0	
	while earlier_month != later_month or earlier_year != later_year:
		earlier_month, earlier_year = GetNextMonth(earlier_month, earlier_year)
		diff += 1
	return diff + 0.5
	
def GetTightestOTMOptions(call, put, price):
	c_diff = 100
	c = 0
	p_diff = 100
	p = 0
	for strike in call.keys():
		c_price = call[strike]
		if c_price - price > 0 and c_price - price < c_diff:
			c_diff = c_price - price	
			c = c_price
	for strike in put.keys():
		p_price = put[strike]
		if p_price - price < 0 and price - p_price < p_diff:
			p_diff = price - p_price	
			p = p_price
	return c, p


if len(sys.argv) != 3:
	print 'USAGE: ' + sys.argv[0] + ' div_min option_price_min'
	sys.exit()

ptConst.logging.info('===== Start a new run of Dividend-Option-Analysis =====')

os.system('rm -f *.opt')
os.system('rm -f *.div')

div_min = float(sys.argv[1])
option_min = float(sys.argv[2])

div_data = StockMap()

for symbol in div_data.stock_map.keys():
	price = div_data.stock_map[symbol].price
	dividend = div_data.stock_map[symbol].dividend
	
	ptConst.logging.info('=== begin analysis for ' + symbol + ', price: ' + str(price) + ', dividend: ' + str(dividend))
	print '\n\n===== PARAMETERS ====='
	print 'stock:', symbol, 'current stock price:', price
	stock = div_data.stock_map[symbol]
	stock.Print()
	if dividend / price < div_min:
		ptConst.logging.info('dividend is ' + str(dividend/price) + ', too small, pass')
		continue
	today = Date()
	opt = DownloadOptionAfterMonth(symbol, 3)
	if opt == '':
		print 'no appropriate options for', symbol, 'pass'	
		continue

	opt_month = int(opt.split('_')[2][:-4])
	opt_year = int(opt.split('_')[1])	
	month_diff = GetMonthDiff(opt_month, opt_year, today.month, today.year)
	ptConst.logging.info('options are expired at ' + GetOptionExpireDate(opt).GetString())
	ptConst.logging.info('dividend within date ' + str(now_year) + '/' + str(now_month) \
			+ ' to ' + str(opt_year) + '/' + str(opt_month) + ' is ' + str(dividend))
	
	call, put = LoadOptionFile(opt, symbol)	
	match_call, match_put = GetTightestOTMOptions(call, put, price)
	ptConst.logging.info('call price:' + str(match_call) + ' put price:' + str(match_put))
	if match_call > option_min or match_put > option_min:
		ptConst.logging.info('==== find a candidate: ' + symbol)

