#! /usr/bin/python

import const

class Transaction:
    
  def __init__(self, symbol, line):
    self.ok = False
    data = line.split(',')
    if data[2] != data[5]: 
      # purchasing date is different then selling date, skip
      print('skip date mismatch')
      return
    self.ok = True 
    cost = data[3]
    sellPrice = data[6]
    # todo cut to 3 digits as splitted transaction could differ sligtly,
    # possibly on the 4th digit
    self.tId = cost + '-' + sellPrice
    self.symbol = symbol 
    self.volume = int(data[1])
    self.date = data[2]
    self.cost = float(data[3])
    self.sellPrice = float(data[6])
    self.gain = float(data[8])

  def __nonzero__(self):
    return self.ok

  def toString(self):
    return 'tId: ' + self.tId \
      + ', symbol: ' + self.symbol \
      + ', date: ' + self.date \
      + ', volume: ' + str(self.volume) \
      + ', cost: ' + str(self.cost) \
      + ', sellPrice: ' + str(self.sellPrice) \
      + ', gain: ' + str(self.gain) \

