#! /usr/bin/python

import ptConst, ptTime, ptTrend

class TrendMaker:
	
	def __init__(self, stockHolder):
		self.stockHolder = stockHolder
	
	def GetTrend(self, startIndex, endIndex, thresh):
		trend = ptTrend.Trend(startIndex, endIndex, thresh)
		startOpen = self.stockHolder.GetEntry(startIndex).Open
		endClose = self.stockHolder.GetEntry(endIndex - 1).Close
		trend.fixType = self.__GetTrendType(startOpen, endClose, thresh)
		
		for index in range(startIndex, endIndex):
			high = self.stockHolder.GetEntry(index).High
			low = self.stockHolder.GetEntry(index).Low
			if self.__GetTrendType(startOpen, high, thresh) == ptConst.BULL_TYPE:
				trend.dynamicBullType = True
			if self.__GetTrendType(startOpen, low, thresh) == ptConst.BEAR_TYPE:
				trend.dynamicBearType = True
			
		return trend
			
	def __GetTrendType(self, start, end, thresh):
		if (end - start) / start > thresh:
			return ptConst.BULL_TYPE
		elif (end - start) / start < -thresh:
			return ptConst.BEAR_TYPE
		else:
			return ptConst.PIG_TYPE
	