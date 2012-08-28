#! /usr/bin/python

import ptConst 

# store a technical analysis value for a day in dict 
class TAData:
    
    data = dict()
    def __init__(self):
        None
        
    def Insert(self, date, value):
        self.data[date] = value
        
    def Print(self):
        for date in self.data:
            print date, self.data[date]
        

