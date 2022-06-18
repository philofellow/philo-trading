#! /usr/bin/python

import const, transaction, report
import sys, os
import csv

#const.logging.info('===== Start Calculating =====')

if len(sys.argv) != 2:
  print('wrong parameters!')
  sys.exit(0)

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

def getExistingTransaction(tIds, transactions):
  for tId in tIds:
    for t in transactions:
      if tId == t.tId:
        return t
  return 'NA'

def processFile(csvFile):
  transactions = [] 
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
        print('not a day trading transaction ', row)
        continue
      existingTransaction = getExistingTransaction(getPossibleSameOrderTIds(txa.tId), transactions)
      if existingTransaction != 'NA':
        print('find an existing transaction that belongs to the same order ', 
                existingTransaction.symbol, existingTransaction.date, existingTransaction.tId)
        # same transaction executed separately
        existingTransaction.volume += txa.volume
        existingTransaction.gain += txa.gain 
      else:
        transactions.append(txa)
  return transactions
          
transactions = processFile(sys.argv[1])
transactions.sort(key=lambda x: x.date, reverse=True)

print('==== Transactions ====')
for t in transactions:
  print(t.toString())

print('==== Report ====')
rp = report.Report(transactions)
print(rp.report)

