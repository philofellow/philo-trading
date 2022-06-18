#! /usr/bin/python

import const, transaction

class Stats:
    
  def __init__(self, transactions):
    self.trades = len(transactions)
    self.win = 0
    self.loss = 0
    self.gain = 0
    for t in transactions:
      self.gain += t.gain
      if t.gain < 0:
        self.loss += 1
      else:
        self.win += 1
    self.winPercent = float(self.win) / self.trades

  def toString(self):
    return 'Trades: ' + str(self.trades) \
      + ', Win: ' + str(self.win) \
      + ', Loss: ' + str(self.loss) \
      + ', winPercent: ' + str(round(self.winPercent, 3)*100) + '%' \
      + ', gain: ' + str(self.gain)
