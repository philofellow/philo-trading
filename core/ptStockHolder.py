#! /usr/bin/python

# StockHolder stores an array of a stocks daily data

import ptConst, ptTime

class StockHolder:

	stockData = [] 

	# load stock data from csv
	def __init__(self, symbol):
		print 'load <' + symbol + '> into StockHolder'
		self.symbol = symbol
		f = open(ptConst.MARKET_DATA_PATH + self.symbol + '.csv', 'r')
		f.readline() # skip first line
		for line in f.readlines():
			line = line.rstrip()
			if not line: break
			line = line.split(',')
			dailyEntry = DailyEntry(ptTime.Date(line[0]).DateInNum(), line[1], 
					line[2], line[3], line[4], line[5])
			if dailyEntry.isValid:
				self.stockData.append(dailyEntry)
		self.stockData = sorted(self.stockData, key=lambda entry: entry.Date)
		
	def Size(self):
		return len(self.stockData)
	
	def GetEntries(self, indexSet):
		data = []
		for id in indexSet:
			data.append(self.stockData[id])
		return data
	def GetEntry(self, index):
		return self.stockData[index]
	
	

	def Print(self):
		print 'stock symbol: <' + self.symbol + '>'
		for entry in self.stockData:
			entry.Print() 

class DailyEntry:

	def __init__(self, Date, Open, High, Low, Close, Volume):
		self.Date = int(Date)
		self.Open = float(Open)
		self.High = float(High)
		self.Low = float(Low)
		self.Close = float(Close)
		self.Volume = int(Volume)
		self.isValid = True
		for price in [self.Open, self.High, self.Low, self.Close]:
			if not self.ValidPrice(price):
				self.isValid = False
		if not self.ValidVolume(self.Volume):
			self.isValid = False
	
	def ValidPrice(self, price):
		if price <= 0:
			return False
		return True
	
	def ValidVolume(self, vol):
		# todo
		if vol <= 0:
			return False
		return True

	def Print(self):
		print 'Date:', self.Date, 'Open:', self.Open, 'High:', self.High, 'Low:', self.Low, \
				'Close:', self.Close, 'Volume:', self.Volume 
