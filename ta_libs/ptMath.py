#! /usr/bin/python

import ptConst, ptStockHolder


class Math:
    
#    def __init__(self):
        
    
    # return average of stock value from beginIndex to endIndex - 1
    @staticmethod
    def Average(stockEntries, valueType):
        value = 0.0
        for entry in stockEntries:
            value += getattr(entry, valueType)
        return value / len(stockEntries)               


