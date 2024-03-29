#!/bin/bash

SYMBOLS='symbols.data'

rm -f $SYMBOLS

for i in "mcc" "psec" "ta" "alsk" "ntwk" "edmc" "pnnt" 
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$i&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price >> $SYMBOLS
done
