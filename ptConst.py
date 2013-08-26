#!/usr/bin/python

import os, sys, logging

sys.path.append('core')
sys.path.append('core/trend')
sys.path.append('utils')
sys.path.append('ta_libs')
sys.path.append('strategies')
sys.path.append('tools')

MARKET_DATA_PATH = './market-data/'
DATA_BEGIN_DATE = '01-jan-90'

BULL_TYPE = 'bull'
BEAR_TYPE = 'bear' 
PIG_TYPE = 'pig'

BUY = 'buy'
SELL = 'sell'
HOLD = 'hold'

logging.basicConfig(format = '%(asctime)s, %(levelname)s, %(message)s', 
                    filename = 'pt.log', level = logging.INFO)

