#! /usr/bin/python

import ptConst, ptMA
from ptStratBase import *

# buy when MA1 up through MA2, sell when MA1 down through MA2
class StratMA2(StratBase):
    
    def __init__(self, taLibs, stockHolder):
        StratBase.__init__(self, taLibs, stockHolder)
        if len(self.taLibs) != 2:
            ptConst.logging.error('StratMA2 must init with two MAs')
            ptConst.sys.exit()
        self.MA1 = taLibs[0]
        self.MA2 = taLibs[1]
        if not self.Validate():
            print 'StratMA2 input ta_libs validation failed'
        self.BuildTrades()
        
    def BuildTrades(self):
        for date in self.taLibDates:
            pDate = self.stock.GetDateOffset(date, -1)
            fDate = self.stock.GetDateOffset(date, 1)
            if pDate == None or fDate == None:
                self.trades[date] = ptConst.HOLD
                continue
            
            pValue1 = self.MA1.GetValue(pDate)
            fValue1 = self.MA1.GetValue(fDate)    
            pValue2 = self.MA2.GetValue(pDate)
            fValue2 = self.MA2.GetValue(fDate)
            # ma1 up through ma2
            if pValue1 < pValue2 and fValue1 > fValue2:
                self.trades[date] = ptConst.BUY
            # ma1 down through ma2
            elif pValue1 > pValue2 and fValue1 < fValue2:
                self.trades[date] = ptConst.SELL
            else:
                self.trades[date] = ptConst.HOLD     
        
    # validate ta libs
    def Validate(self):
        if self.MA1.GetDataSize() != self.MA2.GetDataSize():
            return False
        self.taLibDataSize = self.MA1.GetDataSize()
        self.taLibDates = self.MA1.GetDates()
        None
    def BuyCondition(self):
        None

    def SellCondition(self):
        None
    
    def Print(self):
        for date in self.trades:
            print date, self.trades[date]
    


