#!/usr/bin/python

import time, os, sys, urllib2, random

symbol = ['WMC', 'WHZ', 'CHKR', 'SDT', 'AMTG', 'AGNC', 'CYS', 'SDR', 'IVR']

for s in symbol:
	time.sleep(random.randint(2, 5))
        link = 'http://www.streetinsider.com/dividend_history.php?q=' + s
        filename = s + '.div'
        #data = urllib2.urlopen(link).read()
        os.system('wget ' + link + ' -O ' + filename)



