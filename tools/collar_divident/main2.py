#!/usr/bin/python

# compute max gain, max loss and other property of an investment on a stock, when a collar is applied.
# used for hedge stock volatility, but only to persue dividend
# criterion:
# 1. suppose declaration day is d0, today is d1, ex day is d2, option expiring day is d3
# 2. d1 needs to be within d0 and d2, so a divident is guareentined to be obtained
# 3. d3 needs to be after d2, so the divident eating period is fully protected by the collar
# 4. select the options that d3 is mostly closed to d2, so options premium is the least



import sys, os, math, numpy, datetime, urllib2

SYMBOL_LIST = 'symbols.data'
RANGE = 0.5 # stock price at expiration will be stock_price * (1 - range ) to stock_price * (1 + range)
SAMPLE_SIZE = 10
MAX_LOSS = -0.25

class Date:
	valid = True
	def __init__(self, date_str): # mm/dd/yyyy
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
			self.year = next_date.year + 1
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
		for line in f:
			data = line.split()
			for symbol in data:
				self.LoadDividendData(symbol)

	def Print(self):
		for symbol in self.stock_map.keys():
			print 'symbol: ', symbol
			self.stock_map[symbol].Print()

	def LoadDividendData(self, symbol):
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
		self.stock_map[symbol] = Stock(price, dividend, ex_date, decl_date)
	#	os.system('rm ' + filename)
				
	def LoadProperty(self, line, begin_mark, end_mark):
		begin = line.find(begin_mark) + len(begin_mark)
		end = line[begin:].find(end_mark)
		return line[begin:][:end]


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

def DownloadBestOption(symbol, date):
	tmp_date = date
	for i in range(3): # take the options expiring at most 3 month later than the ex_div_date
		opt = DownloadOption(symbol, tmp_date.month, tmp_date.year)
		if IsEmptyOptionFile(opt, symbol):
			print 'empty option file:', opt
			os.system('rm ' + opt)
			tmp_date.MoveToNextMonth()
			continue
		if OptionExpireLaterThanDate(opt, date):
			return opt
		else:
			print 'options expires earlier than ex_div_date:', date.GetString()  
			os.system('rm ' + opt)
			tmp_date.MoveToNextMonth()
	
	return ''
			

def GetPriceSamples(price, rg, num):
	min = price * (1 - rg)
	max = price * (1 + rg)
	step = (max - min) / num
	return numpy.arange(min, max, step)

def ComputeYield(c_strike, c_price, p_strike, p_price, price, dividend, months):
	cost = price - c_price + p_price 
	p_to_yield = dict()
	for p in GetPriceSamples(price, RANGE, SAMPLE_SIZE):
		if p >= c_strike:
			revenue = c_strike + dividend
		elif p < c_strike and p > p_strike:
			revenue = p + dividend
		else:
			revenue = p_strike + dividend
		
		profit = revenue - cost	
		term_yield = profit / cost
		annualized_yield = math.pow((1 + term_yield), 12.0 / months) - 1
		if annualized_yield < MAX_LOSS:
			return None 
		p_to_yield[p] = (profit, term_yield, annualized_yield)		
	return p_to_yield


def DownloadOption(symbol, month, year):

	link = 'http://www.optionpain.altervista.org/csv.php?symbol=' \
			+ symbol + '&month=' + str(month) + '&year=' + str(year)

	print 'download <' + symbol + '> from ' + link
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
	return diff

def DateMatch(past, future):
	today = str(datetime.date.today()).split('-')
	day = today[2]
	month = today[1]
	year = today[0]
	now = Date(month + '/' + day + '/' + year)
	return past < now and now < future

if len(sys.argv) != 1:
	print 'USAGE: ./main.py'
	sys.exit()

os.system('rm *.opt')
os.system('rm *.div')

div_data = StockMap()

for symbol in div_data.stock_map.keys():
	price = div_data.stock_map[symbol].price
	dividend = div_data.stock_map[symbol].dividend

	print '\n\n===== PARAMETERS ====='
	print 'stock:', symbol
	print 'current stock price:', price
	stock = div_data.stock_map[symbol]
	stock.Print()
	if not DateMatch(stock.decl_date, stock.ex_date):
		print 'date not match, pass'
		continue
	opt = DownloadBestOption(symbol, stock.ex_date)
	if opt == '':
		print 'not appropriate options for', symbol, 'pass the analysis'	
		continue
	print 'option file:', opt 

	opt_month = int(opt.split('_')[2][:-4])
	opt_year = int(opt.split('_')[1])	
	now_month = int(str(datetime.date.today()).split('-')[1])
	now_year = int(str(datetime.date.today()).split('-')[0])
	month_diff = GetMonthDiff(opt_month, opt_year, now_month, now_year)
	print 'options are expired at', GetOptionExpireDate(opt).GetString(), 'which is', month_diff, 'months later'
	print 'dividend within date ' + str(now_year) + '/' + str(now_month) + ' to ' + str(opt_year) + '/' + str(opt_month) + ' is ' + str(dividend)

	call, put = LoadOptionFile(opt, symbol)	
	print '===== YIELD TABLE ====='

	for c_strike in call.keys():
		if c_strike > price:
			for p_strike in put.keys():
				if p_strike < price:
					print '----- c_strike:', c_strike, 'p_strike:', p_strike, 'c_price:', call[c_strike], 'p_price:', put[p_strike]
					yield_table = ComputeYield(c_strike, call[c_strike], p_strike, put[p_strike], price, dividend, month_diff)
					if yield_table is None:
						print 'exceeds max loss, drop'
					else:					
						for p in sorted(yield_table.keys()):
							print 'future price: ' + p \
									+ ', profit: ' + yield_table[p][0] \
									+ ', term yield: ' + yield_table[p][1] \
									+ 'annualized yield: ' + yield_table[p][2]

