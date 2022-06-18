#! /usr/bin/python

import const

class Transaction:
    
  def __init__(self, data):
    self.ok = False
    print data
    if data[2] != data[6]: 
      # purchasing date is different then selling date, skip
      print('skip date mismatch')
      return
    self.ok = True 
    # todo cut to 3 digits as splitted transaction could differ sligtly,
    # possibly on the 4th digit
    self.symbol = data[0] 
    self.volume = int(data[1].replace('"', '').replace(',', ''))
    self.date = data[2]
    self.cost = float(data[3])
    self.sellPrice = float(data[7])
    self.gain = float(data[9])
    self.tId = str(self.cost) + '-' + str(self.sellPrice)

  def __nonzero__(self):
    return self.ok

  def toString(self):
    return 'tId: ' + self.tId \
      + ', symbol: ' + self.symbol \
      + ', date: ' + self.date \
      + ', volume: ' + str(self.volume) \
      + ', cost: ' + str(self.cost) \
      + ', sellPrice: ' + str(self.sellPrice) \
      + ', gain: ' + str(self.gain) 

