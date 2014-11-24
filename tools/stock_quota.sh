#!/bin/bash

echo "===== queried quotas ====="
for sym in $@
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$sym&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price
done;

echo "===== default quotas ====="

for i in "mcc" "psec" "ta" "alsk" "ntwk" "edmc" "pnnt" "gov"
do
	p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$i&f=nsl1p2'"`
	price=`eval $p`;
	echo $(date +'%Y/%m/%d %H:%M') $price
done
