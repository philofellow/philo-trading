#!/bin/bash

p=`printf "curl -s 'http://download.finance.yahoo.com/d/quotes.csv?s=$1&f=l1'"`
price=`eval $p`;
echo $price
