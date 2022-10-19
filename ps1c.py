# I had alot of difficulty with this problem and, in the end, could not
# complete it on my own. I spent a lot of time on stack overflow, github and 
# reddit looking for solutions and ended up essentially copying this source:
# https://www.reddit.com/r/learnpython/comments/6bdbxq/mit_60001_introduction_to_cs_with_python_fall/

# I rewrote the variable names and studied it to help me understnand and
# believe that I have it mostley figured out. However, I still don't beleive
# I would be capable of coming up with this on my own as of the time of this submission





starting_salary = input('Enter the starting salary: ')

semi_annual_raise = 0.07
annual_return = 0.04
house_cost = 1000000
down_payment_percentage = 0.25

savings_needed = down_payment_percentage*house_cost

high = 10000
low = 0
savings = 0
num_guesses = 0

while high - low > 2 and num_guesses < 30:
    decimal_guess = int((high + low)/2)
    savings_rate = decimal_guess/10000
    savings = 0
    salary = starting_salary
    for months in range(1,37):
        savings_return =  (savings * annual_return)/12
        savings_per_month = float(salary)/12
        savings += savings_rate * savings_per_month + savings_return
        if months % 6 == 0:
            salary = float(salary) * (1 + semi_annual_raise)
        #print(savings)
    if savings < savings_needed:
        low = decimal_guess
        #print('low:', low)
    elif savings > savings_needed:
        high = decimal_guess
        #print('high', high)
    num_guesses +=1
    #print(num_guesses)

print('Best savings rate:', savings_rate)
print('Steps in bisection search:', num_guesses)