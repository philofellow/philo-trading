#!/usr/bin/python

'''
the class stores date internally
e.g.:
d = Date() # d stores date for now
d = Date('10-aug-12') # d stores a specific date

'''

import ptConst, datetime

class Date:

	monMap = {'jan':'01', 'feb':'02', 'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 
			'jul':'07',	'aug':'08', 'sep':'09', 'oct':'10', 'nov':'11', 'dec':'12'}
	
	monList = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
	
	def __init__(self, date=None):
		if date:
			day, mon, year = date.split('-')
			self.dayInNum = self.__GetDayFormat(day)
			self.monInNum = self.__GetMonFormat(mon.lower())
			self.monInChar = mon.lower()
			self.yearInNum = self.__GetYearFormat(year)
		else:
			now = datetime.datetime.now()
			self.dayInNum = now.strftime("%d")
			self.monInNum = now.strftime("%m")
			self.monInChar = self.monList[int(self.monInNum)-1]
			self.yearInNum = now.strftime("%Y")
			
	# return yyyymmdd
	def DateInNum(self):
		return self.yearInNum + self.monInNum + self.dayInNum
	
	# return dd-mon-yy
	def DateInChar(self):
		return self.dayInNum + '-' + self.monInChar + '-' + self.yearInNum
		
	def __GetDayFormat(self, day):
		if len(day) == 1:
			day = '0' + day
		return day

	def __GetMonFormat(self, mon):
		return self.monMap[mon]

	def __GetYearFormat(self, year):
		if int(year) < 13:
			year = '20' + year
		else:
			year = '19' + year
		return year
