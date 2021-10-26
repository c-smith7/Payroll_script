# function to calculate payroll amount, including overtime. 

def payroll(pay_rate, hours):
    if hours > 80:
        amount = 80 * pay_rate + ((hours-80) * (pay_rate*1.5))
        return amount
    else:
        amount = pay_rate * hours
        return amount