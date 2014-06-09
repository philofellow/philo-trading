#!/bin/bash

p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$1&f=nsl1p2'"`
price=`eval $p`;
echo $(date +'%Y/%m/%d %H:%M') $price
