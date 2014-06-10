#!/usr/bin/python

import sys, os, math

if len(sys.argv) != 1:
	print 'USAGE:', sys.argv[0]
	sys.exit()

rent_m = 1450 # rent per month
vacancy = 4 # weeks of vacancy per year
hoa_m = 370 # hoa fee per month
insurance_y = 400 # all property insurance per year
house_price = 135000 # property price
downpay = 0.25 # down payment
upfront_cost = 5000 # closing + refurnish
int_y = 0.0575 # yearly mortgage interest 
period_y = 30 # loan period in years
tax_rate = 0.01 # property tax rate
inflation = 0.02 # property value increase yearly
maintain = 0.1 # maintainess cost in percent of rent
#agent_fee = rent_m / 12.0 # if use agent to manage
agent_fee = 0 

int_m = int_y / 12
period_m = period_y * 12
loan = house_price * (1 - downpay)

mortgage_pay_m = loan * (int_m / (1 - math.pow((1 + int_m), -period_m)))
tax_m = house_price * tax_rate / 12

equity_start = house_price * downpay
init_inv = equity_start + upfront_cost # initial investment 

# cost: hoa, insurance, property tax, mortgate payment, maintainess cost, vacancy, management fee
fixed_cost_m = hoa_m + insurance_y / 12 + tax_m + mortgage_pay_m 
vari_cost_m = rent_m * maintain + rent_m * vacancy / 52.0 + agent_fee
cost_m = fixed_cost_m + vari_cost_m 

cash_flow = rent_m - cost_m 
principle_pay_m = mortgage_pay_m / 2 # roughly estimate principle payment as a proportion of mortgage payment 
house_value_inc_m = house_price * inflation / 12

profit_m = cash_flow + principle_pay_m + house_value_inc_m
return_y = profit_m * 12 / init_inv 

print 'loan payment per month: ' + str(mortgage_pay_m)
print 'principle payment per month: ' + str(principle_pay_m)
print 'fixed cost per month (hoa, insurance, mortgage pay, tax): ' + str(fixed_cost_m)
print 'variable cost per month (maintainess, vacancy, management): ' \
	+ str(rent_m * maintain) + ' + ' \
	+ str(rent_m * vacancy / 52.0) + ' + ' \
	+ str(agent_fee) + ' = ' \
	+ str(vari_cost_m)
print 'cost per month: ' + str(cost_m)
print 'rent per month: ' + str(rent_m)
print 'cashflow per month: ' + str(cash_flow)
print 'house value increase per month: ' + str(house_value_inc_m)
print 'profit per month: ' + str(profit_m)
print 'initial investment: ' + str(init_inv)
print 'cash return annually: ' + str(cash_flow * 12 / init_inv)
print 'total return annually: ' + str(return_y)

