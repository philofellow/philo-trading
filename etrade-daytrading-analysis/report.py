#! /usr/bin/python

import const, stats, transaction

class Report:
   
  def __init__(self, transactions):
      self.report = 'Summary:\n'  
      # overall result
      self.report += stats.Stats(transactions).toString() + '\n'

      # daily result
      self.report += '\nDaily Results:\n'  
      dailyRes = dict()
      for t in transactions:
        if t.date not in dailyRes:
          dailyRes[t.date] = [] 
        dailyRes[t.date].append(t)

      for d in sorted(dailyRes):
        self.report += d + ': '
        s = stats.Stats(dailyRes[d])
        self.report += s.toString() + '\n'
