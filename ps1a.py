# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:38:52 2022

@author: jorda
"""
#Part A of Problem Set 1

#inputs
annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = float(input('Enter the cost of your dream home: ' ))

#static values
portion_down_payment = (0.25*total_cost)
r = 0.04
monthly_salary = annual_salary/12

#values affected by loop
current_savings = 0
n_of_months = 0

#loop that calculates the number of months required to reach the amount needed for down payment
while current_savings < portion_down_payment:
    monthly_return = current_savings*r/12
    current_savings = current_savings + ((monthly_salary*portion_saved) + monthly_return)
    n_of_months = n_of_months + 1

print('Number of months: ', n_of_months)
print('Number of years: ', n_of_months/12)