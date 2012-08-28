#! /usr/bin/python

import sys
sys.path.append('core')
sys.path.append('core/trend')
sys.path.append('utils')
sys.path.append('ta_libs')

import ptConst, ptStockHolder, ptDataDownloader, ptTrendMaker
import ptMA

#ptDataDownloader.DownloadStock('spy', '01-aug-12', '10-aug-12')
#ptDataDownloader.DownloadStock('spy')

sh = ptStockHolder.StockHolder('spy')
sh.Print()

#ma5 = ptMA.MA(sh, 5)
#ma5.Print()

tm = ptTrendMaker.TrendMaker(sh)
trend = tm.GetTrend(0, 5, 0.01)
trend.Print()