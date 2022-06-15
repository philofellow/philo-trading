#! /usr/bin/python

import const, transaction, report
import sys, os

const.logging.info('===== Start Calculating =====')

if len(sys.argv) != 2:
  print('wrong parameters!')
  sys.exit(0)

def summary(transactions):
  res = dict() 
  for t in transactions:
      if t.date not in res:
         res[t.date] = dict()

# consider 12.34-13.45 and 12.35-13.44 the same tId as it could be the single
# order that is splitted
def getSameTId(tId):
  [buy,sell] = tId.split('-')
  #print buy, sell
  buy = float(buy)
  sell = float(sell)
  res = []
  res.append(str(buy) + '-' + str(sell))
  res.append(str(buy) + '-' + str(sell + 0.01))
  res.append(str(buy) + '-' + str(sell - 0.01))
  res.append(str(buy + 0.01) + '-' + str(sell))
  res.append(str(buy - 0.01) + '-' + str(sell))
  res.append(str(buy + 0.01) + '-' + str(sell + 0.01))
  res.append(str(buy + 0.01) + '-' + str(sell - 0.01))
  res.append(str(buy - 0.01) + '-' + str(sell + 0.01))
  res.append(str(buy - 0.01) + '-' + str(sell - 0.01))
  return res

def getExistingTId(tIds, transactions):
  for tId in tIds:
    if tId in transactions:
      return tId
  return 'NA'

def processFile(f):
  transactions = dict()
  toRead = False 
  for line in open(f).readlines():
    if line.startswith('Total,'):
      toRead = False 
      continue
    if line.startswith('Symbol,'):
      toRead = True 
      continue
    if not toRead:
      continue
    #print(line)
    if line.startswith(' '):
      # transaction line
      txa = transaction.Transaction(symbol, line)
      if not txa:
        print('none object')
        continue
      existingTId = getExistingTId(getSameTId(txa.tId), transactions)
      if existingTId != 'NA':
        print('process')
        # same transaction executed separately
        transactions[existingTId].volume += txa.volume
        transactions[existingTId].gain += txa.gain 
      else:
        transactions[txa.tId] = txa
    else:
      print('reading symbol line ' + line)
      symbol = line.split(',')[0]
  return transactions
          
transactions = processFile(sys.argv[1])
for t in transactions:
  print(transactions[t].toString())

rp = report.Report(transactions)
print(rp.report)





