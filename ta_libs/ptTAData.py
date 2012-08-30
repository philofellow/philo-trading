#! /usr/bin/python

import ptConst 

# store a technical analysis value for a day in dict {date:value}
class TAData:
    
    data = dict()
    def __init__(self):
        None
        
    def Insert(self, date, value):
        self.data[date] = value
        
    def GetValue(self, date):
        if date in self.data:
            return self.data[date]
        else:
            return None
    
    def Size(self):
        return len(self.data.keys())
        
    def Print(self):
        for date in self.data:
            print date, self.data[date]
        

