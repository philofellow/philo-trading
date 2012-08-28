#! /usr/bin/python

import ptConst, urllib2, ptTime 
    
def __DStock(bDate, eDate, symbol):  
    bDay, bMon, bYear = bDate.dayInNum, bDate.monInChar, bDate.yearInNum;
    eDay, eMon, eYear = eDate.dayInNum, eDate.monInChar, eDate.yearInNum;

    link = 'http://www.google.com/finance/historical?' \
            'q=' + symbol + '&' \
            'startdate=' + bMon + '+' + bDay + '%2C+' + bYear + '&' \
            'enddate=' + eMon + '+' + eDay + '%2C+' + eYear + '&' \
            'output=csv'
            
    print 'download <' + symbol + '> from google: \n' + link
     
    csv = urllib2.urlopen(link).read()

    f = open(ptConst.MARKET_DATA_PATH + symbol + '.csv', 'w')
    f.write(csv)

# download daily price from google and store in a csv file
def DownloadStock(symbol, beginDate=None, endDate=None):
    if beginDate:
        __DStock(ptTime.Date(beginDate), ptTime.Date(endDate), symbol)
    else:
        __DStock(ptTime.Date(ptConst.DATA_BEGIN_DATE), ptTime.Date(), symbol)   
  

    
    


