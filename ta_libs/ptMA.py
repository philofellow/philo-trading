#! /usr/bin/python

import ptConst, ptMath, ptTAData

class MA:
    
    def __init__(self, stockHolder, param):
        self.stock = stockHolder
        self.param = param
        self.taData = ptTAData.TAData()
        for i in range(self.stock.Size() - param + 1):
            indexSet = []
            for j in range(i, i + param):
                indexSet.append(j)
            data = self.stock.GetEntries(indexSet)
            close = ptMath.Math.Average(data, 'Close')
            self.taData.Insert(self.stock.GetEntry(i + param - 1).Date, close)
    
    def Print(self):
        self.taData.Print()
    
    


