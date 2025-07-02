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
```
```

# Resources
https://marketchameleon.com/volReports/VolatilityRankings
