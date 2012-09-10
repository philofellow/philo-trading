#! /usr/bin/python

import ptConst, ptMath, ptTAData, ptStockHolder
from ptTALibBase import *

# moving average of the stock for param days, e.g., MA5, MA10, etc.
class MA(TALibBase):
    
    def __init__(self, stockHolder, param):
        ptConst.logging.info('create MA %d with close price for <%s>', 
                             param, stockHolder.symbol)
        TALibBase.__init__(self, stockHolder, param)
        for i in range(self.stock.Size() - param + 1):
            indexSet = []
            for j in range(i, i + param):
                indexSet.append(j)
            data = self.stock.GetEntries(indexSet)
            close = ptMath.Math.Average(data, 'Close')
            self.taData.Insert(self.stock.GetEntry(i + param - 1).Date, close)

    
    


