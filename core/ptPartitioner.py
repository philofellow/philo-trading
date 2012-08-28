#! /usr/bin/python


import ptConst, ptTime, ptTrend

class TrendMaker:
	
	def __init__(self, stockHolder):
		self.stockHolder = stockHolder
	
	def MakeTrend(self, startIndex, endIndex, thresh):
		trend = ptTrend.Trend(startIndex, endIndex, thresh)
		startClose = stockHolder.GetEntry(startIndex).Close
		endClose = stockHolder.GetEntry(startIndex - 1).Close
		type = __GetTrendType(startClose, endClose, thresh)
		
		for index in range(startIndex, endIndex):
			close = stockHolder.GetEntry(index).Close
			high = stockHolder.GetEntry(index).High
			low = stockHolder.GetEntry(index).Low
			
			if
	def __GetTrendType(self, start, end, thresh):
		if (end - start) / start > thresh:
			return ptConst.BULL_TYPE
		else if (end - start) / start < -thresh:
			return ptConst.BEAR_TYPE
		else return ptConst.PIG_TYPE