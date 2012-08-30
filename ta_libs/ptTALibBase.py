#! /usr/bin/python

import ptConst, ptMath, ptTAData

# moving average of the stock for param days, e.g., MA5, MA10, etc.
class TALibBase:
    
    def __init__(self, stockHolder, param):
        self.stock = stockHolder
        self.param = param
        self.taData = ptTAData.TAData()
        
    def GetValue(self, date):
        return self.taData.GetValue(date)
    
    def GetDataSize(self):
        return self.taData.Size()
    
    def GetDates(self):
        return self.taData.data.keys()
    
    def Print(self):
        print 'printing TA lib:', self.__class__.__name__, 'param:', self.param    
        self.taData.Print()
    
    


