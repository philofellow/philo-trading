#!/bin/bash

echo "===== queried quotas ====="
for sym in $@
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$sym&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price
done;

echo "===== indexes ====="

for i in "^gspc" "^vix"
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$i&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price
done

echo "===== portfolio ====="

for i in "mcc" "gov" "bdcl" "ta" "alsk" "ntwk" "grbk"
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$i&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price
done

echo "===== watchlist ====="

for i in "pnnt" "baba" 
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$i&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price
done
