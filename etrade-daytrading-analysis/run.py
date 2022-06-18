#! /usr/bin/python

import const, transaction, report
import sys, os
import csv

#const.logging.info('===== Start Calculating =====')

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
def getPossibleSameOrderTIds(tId):
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

def processFile(csvFile):
  transactions = dict()
  toRead = False 
  with open(csvFile) as f:
    reader = csv.reader(f)
    for row in reader:
      if row[0] == 'Symbol':
        toRead = True 
        continue
      if not toRead:
        continue
      #print(line)
      # transaction line
      txa = transaction.Transaction(row)
      if not txa:
        print('not a day trading transaction')
        continue
      existingTId = getExistingTId(getPossibleSameOrderTIds(txa.tId), transactions)
      if existingTId != 'NA':
        print('find an existing transaction that belongs to the same order')
        # same transaction executed separately
        transactions[existingTId].volume += txa.volume
        transactions[existingTId].gain += txa.gain 
      else:
        transactions[txa.tId] = txa
  return transactions
          
transactions = processFile(sys.argv[1])
print('==== Transactions ====')
for t in transactions:
  print(transactions[t].toString())

print('==== Report ====')
rp = report.Report(transactions)
print(rp.report)





