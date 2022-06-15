#! /usr/bin/python

import const, stats, transaction

class Report:
   
  def __init__(self, transactions):
      self.report = 'Summary:\n'  
      # overall result
      self.report += stats.Stats(transactions).toString() + '\n'

      # daily result
      dailyRes = dict()
      for t in transactions:
        tx = transactions[t]
        if tx.date not in dailyRes:
          dailyRes[tx.date] = dict()
        dailyRes[tx.date][tx.tId] = tx

      for d in sorted(dailyRes):
        self.report += d + ': '
        s = stats.Stats(dailyRes[d])
        self.report += s.toString() + '\n'
