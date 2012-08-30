#! /usr/bin/python

import sys
sys.path.append('core')
sys.path.append('core/trend')
sys.path.append('utils')
sys.path.append('ta_libs')
sys.path.append('strategies')

import ptConst, ptStockHolder, ptDataDownloader, ptTrendMaker
import ptMA, ptStratMA2

#ptDataDownloader.DownloadStock('spy', '01-aug-12', '10-aug-12')
#ptDataDownloader.DownloadStock('spy')

sh = ptStockHolder.StockHolder('spy')
sh.Print()

tm = ptTrendMaker.TrendMaker(sh)
trend = tm.GetTrend(0, 5, 0.01)
trend.Print()

ma5 = ptMA.MA(sh, 5)
ma5.Print()

ma10 = ptMA.MA(sh, 10)
ma10.Print()

stratMA2 = ptStratMA2.StratMA2([ma5, ma10], sh)
stratMA2.Print()