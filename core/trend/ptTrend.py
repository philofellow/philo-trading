#! /usr/bin/python


import ptConst

# a short period of bull or bear or pig market
class Trend:
	startIndex = 0
	endIndex = startIndex + 5
	
	# price of last day is higher than first day for threshhold
	fixType = ptConst.PIG_TYPE
	
	# price of any day in the period is higher than first day for threshhold
	dynamicBullType = False
	# price of any day in the period is lower than first day for threshhold
	dynamicBearType = False
	#todo volatility
	
	thresh = 0.1 # percentage of up or down
	
	def __init__(self, startIndex=None, endIndex=None, thresh=None):
		self.startIndex = startIndex
		self.endIndex = endIndex
		self.thresh = thresh
		
	def Print(self):
		print 'start index: ' + str(self.startIndex) + ', end index: ' + str(self.endIndex)
		print 'fix type: ' + self.fixType + ', dynamic bull: ' + str(self.dynamicBullType) \
				+ ', dynamic bear: ' + str(self.dynamicBearType)
