#! /usr/bin/python

import const, transaction

class Stats:
    
  def __init__(self, transactions):
    self.totalNum = len(transactions)
    self.totalWinNum = 0
    self.totalLossNum = 0
    self.gain = 0
    for t in transactions:
      self.gain += transactions[t].gain
      if transactions[t].gain < 0:
        self.totalLossNum += 1
      else:
        self.totalWinNum += 1
    self.winPercent = float(self.totalWinNum) / self.totalNum

  def toString(self):
    return 'totalNum: ' + str(self.totalNum) \
      + ', totalWinNum: ' + str(self.totalWinNum) \
      + ', totalLossNum: ' + str(self.totalLossNum) \
      + ', winPercent: ' + str(self.winPercent) \
      + ', gain: ' + str(self.gain)
