#!/usr/bin/python

import sys, os, math

if len(sys.argv) != 1:
	print 'USAGE:', sys.argv[0]
	sys.exit()

rent_m = 1250.0 # rent per month
vacancy = 4.0 # weeks of vacancy per year
hoa_m = 270.0 # hoa fee per month
insurance_y = 400.0 # all property insurance per year
house_price = 115000.0 # property price
downpay = 0.25 # down payment
upfront_cost = 5000.0 # closing + refurnish
int_y = 0.0475 # yearly mortgage interest 
period_y = 30.0 # loan period in years
tax_rate = 0.01 # property tax rate
inflation = 0.03 # property value increase yearly
maintain = 0.1 # maintainess cost in percent of rent
#agent_fee = rent_m / 12.0 # if use agent to manage
agent_fee = 0.0 

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
cash_return_y = cash_flow * 12 / init_inv
principle_pay_m = mortgage_pay_m / 2 # roughly estimate principle payment as a proportion of mortgage payment 
house_value_inc_m = house_price * inflation / 12

profit_m = cash_flow + principle_pay_m + house_value_inc_m
return_y = profit_m * 12 / init_inv 

print ('= rent per month: %.1f' % rent_m)
print ('= total cost per month: %.1f' % cost_m)
print ('=== fixed cost per month: %.1f (hoa %.1f, insurance %.1f, mortgage pay %.1f, tax %.1f)' % \
	(fixed_cost_m, hoa_m, insurance_y / 12, mortgage_pay_m, tax_m))
print ('=== variable cost per month: %.1f (maintainess %.1f, vacancy(%d weeks) %.1f, management %.1f)' % \
	(vari_cost_m, rent_m * maintain, vacancy, rent_m * vacancy / 52.0, agent_fee))
print ('= cashflow per month: %.1f' % cash_flow)
print ('= principle payment per month: %.1f' % principle_pay_m)
print ('= house value increase per month: %.1f' % house_value_inc_m)
print ('+++ profit per month: %.1f' % profit_m)
print ('initial investment: %.1f' % init_inv)
print ('cash return annually: %.1f%%' % (cash_return_y * 100))
print ('total return annually: %.1f%%' % (return_y * 100))

