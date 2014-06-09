#!/usr/bin/python

import sys, os, math

if len(sys.argv) != 1:
	print 'USAGE:', sys.argv[0]
	sys.exit()

rent_m = 1000
hoa_m = 270
insurance_y = 300
house_price = 115000
downpay = 0.25
upfront_cost = 5000 # closing + refurnish
int_y = 0.0475
period_y = 30
tax_rate = 0.01
inflation = 0.07

int_m = int_y / 12
period_m = period_y * 12
loan = house_price * (1 - downpay)

pay_m = loan * (int_m / (1 - math.pow((1 + int_m), -period_m)))
tax_m = house_price * tax_rate / 12

equity_start = house_price * downpay
cost = equity_start + upfront_cost

cost_m = hoa_m + insurance_y / 12 + tax_m + pay_m
cash_flow = rent_m - cost_m 
principle_pay_m = pay_m / 2 
house_value_inc_m = house_price * inflation / 12


profit_m = cash_flow + principle_pay_m + house_value_inc_m
return_y = profit_m * 12 / cost

print 'loan payment per month: ' + str(pay_m)
print 'principle payment per month: ' + str(principle_pay_m)
print 'cost per month: ' + str(cost_m)
print 'rent per month: ' + str(rent_m)
print 'cashflow per month: ' + str(cash_flow)
print 'house value increase per month: ' + str(house_value_inc_m)
print 'profit per month: ' + str(profit_m)
print 'initial cost: ' + str(cost)
print 'return annually: ' + str(return_y)

