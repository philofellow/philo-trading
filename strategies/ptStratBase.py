#! /usr/bin/python

import ptConst, ptTALibBase

class StratBase:
    
    trades = dict()
    
    def __init__(self, taLibs, stockHolder):
        self.stock = stockHolder
        self.taLibs = taLibs
    
    def BuyCondition(self):
        None
    def SellCondition(self):
        None
    def BuildTrades(self):
        None
    
    def Print(self):
        None
    


