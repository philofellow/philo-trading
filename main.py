#! /usr/bin/python

import ptConst
import ptStockHolder, ptDataDownloader, ptTrendMaker
import ptMA, ptStratMA2

ptConst.logging.info('===== Start a new run of PT-Trader =====')

#ptDataDownloader.DownloadStock('spy', '01-aug-01', '10-aug-12')
ptDataDownloader.DownloadStock('INDEXCBOE%3AVIX')

sh = ptStockHolder.StockHolder('INDEXCBOE%3AVIX')
sh.Print()

tm = ptTrendMaker.TrendMaker(sh)
trend = tm.GetTrend(0, 5, 0.01)
trend.Print()
'''
ma5 = ptMA.MA(sh, 5)
ma5.Print()

ma10 = ptMA.MA(sh, 10)
ma10.Print()

stratMA2 = ptStratMA2.StratMA2([ma5, ma10], sh)
stroatMA2.Print()
'''
