# Dependencies

```
pip install --upgrade yfinance
```

# Run
```
python main.py > res-russell3000-$(date +\%Y\%m\%d) 2>> error.log
```

# crontab
```
0 17 * * * cd /home/philofellow/workspace/philo-trading/strategies/sell-put && python main.py > result/res-russell3000-$(date +\%Y\%m\%d) 2>> error.log
```

# grep result

To grep next Friday expiring options and get rid of those with $0 bid. 
```
grep "\*" result/res-russell3000-20250710 | grep 2025-07-18 | grep -v "0.00 " | less
```

# Resources
https://marketchameleon.com/volReports/VolatilityRankings
