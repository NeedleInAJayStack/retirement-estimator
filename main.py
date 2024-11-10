import argparse
from sympy import *
from datetime import *

parser = argparse.ArgumentParser(
  prog='retirement_estimator',
  description='''
  Estimates net worth throughout time based on current net worth, income, spending, retirement date, and investment returns.

  It will output:
  - The estimated net worth at retirement and the target date (if provided)
  - The break-even net worth, at which you could sustain your retirement spending off returns alone
  - The estimated age at which the break-even net worth is achieved, and at which the target worth is achieved (if provided)
  - A chart showing the estimated net worth over time

  The results of this calculator are not a guarantee of future performance. Consult a financial advisor for personalized advice.

  Assumptions:
  - This model assumes constant investment returns, not realistic/historical market fluctuation. Choose return rates accordingly.
  - Inflation is not accounted for in this model. It should be accounted for in the investment return rates.
  - All non-spent money is assumed to be invested and earns the return rate.
  - Return rates are assumed to be on total net worth, not necessarily assets. If your assets are significantly leveraged with debt, this may cause inaccuracies.
  ''',
  formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument('-b', '--birthdate', type=str, help='Birthday', required=True)
parser.add_argument('-w', '--net-worth', type=int, help='Current net worth', required=True)
parser.add_argument('-wd', '--net-worth-date', type=str, help='Current net worth date. Assumed to be today', required=False)
parser.add_argument('-wi', '--working-salary', type=int, help='Average working salary', required=True)
parser.add_argument('-wr', '--working-investment-return', type=float, help='Investment return during working years', default=0.06, required=False)
parser.add_argument('-ws', '--working-spending', type=int, help='Average working spending', required=True)
parser.add_argument('-r', '--retirement-age', type=int, help='Retirement age in years', required=True)
parser.add_argument('-ri', '--retired-salary', type=int, help='Average retirement salary. Assumed to be 0', default=0, required=False)
parser.add_argument('-rr', '--retired-investment-return', type=float, help='Investment return during retirement years', default=0.04, required=False)
parser.add_argument('-rs', '--retired-spending', type=int, help='Average retirement spending', required=True)
parser.add_argument('-td', '--target-date', type=str, help='If included, a target date for which to print the net worth', required=False)
parser.add_argument('-tw', '--target-worth', type=int, help='If included, a target worth for which to print the date', required=False)
args = parser.parse_args()

birthdate = datetime.strptime(args.birthdate, '%Y-%m-%d').date()
worth_0 = args.net_worth
date_0 = datetime.strptime(args.net_worth_date, '%Y-%m-%d').date() if args.net_worth_date else date.today()
working_salary = args.working_salary
working_inv_return = args.working_investment_return
working_spending = args.working_spending
retirement_age = args.retirement_age
retired_salary = args.retirement_age
retired_inv_return = args.retired_investment_return
retired_spending = args.retired_spending

age_0 = (date_0 - birthdate) / timedelta(days = 365.25)

def ageToDate(age):
  return birthdate + timedelta(days = int(age * 365.25))


# The key to this is a differential equation: dy/dt = r*y + a  =>  y = Ae^(rt) - a/r, where A is a constant based on the starting sum, r is the annual return,
# and a is the net yearly saving/spending not related to returns on investment.
# The first part of this can be derived from the y=Ae^rt continuously compounding interest equation and the intuition behind the "+ a" is that the non-interest slope is constant.
age = Symbol('age')
worth_work = (worth_0 + (working_salary-working_spending)/working_inv_return) * exp(working_inv_return*(age-age_0)) - (working_salary-working_spending)/working_inv_return
worth_ret = (worth_work.subs(age, retirement_age) + (retired_salary-retired_spending)/retired_inv_return) * exp(retired_inv_return*(age-retirement_age)) - (retired_salary-retired_spending)/retired_inv_return
# Computes the worth at any given age. The piecewise function is necessary to account for the different investment returns during working and retirement years.
worth_by_age = Piecewise((worth_work, age <= retirement_age), (worth_ret, age > retirement_age)) # Don't let it go beneath 0, cause the interest gets weird.

print(f'Est worth at retirement: ${worth_ret.subs(age, retirement_age):,.0f}')
if args.target_date:
  targetDate = datetime.strptime(args.target_date, '%Y-%m-%d').date()
  targetAge = (targetDate - birthdate) / timedelta(days = 365.25)
  print(f'Est worth on {targetDate}: ${worth_by_age.subs(age, targetAge):,.0f}')
print('')

worth = Symbol('worth')
# Computes the age at which the input worth is achieved. Just the inverse of worth_work. Only valid during working years b/c breaking up the piecewise is complicated.
age_by_worth = ln((worth + (working_salary-working_spending)/working_inv_return)/(worth_0 + (working_salary-working_spending)/working_inv_return)) / working_inv_return + age_0
# The retirement "break-even" amount is -1*(retired_salary-retired_spending)/annualReturn.
# So for no retirement income, $20000 in spending and a 6% return, you must have $333,333 to live forever without ever increasing/decreasing.
break_even_worth = -1*(retired_salary-retired_spending)/retired_inv_return
print(f'Break-even amount: ${break_even_worth:,.0f}')
break_even_age = age_by_worth.subs(worth, break_even_worth)
print(f'Est break-even age: {break_even_age:.2f} / {ageToDate(break_even_age)}')
if args.target_worth:
  targetWorth = args.target_worth
  targetAge = age_by_worth.subs(worth, targetWorth)
  print(f'Est age at ${targetWorth:,.0f} (if still working): {targetAge:.2f} / {ageToDate(targetAge)}')

# Plot worth over time
plot(worth_by_age, (age, age_0, 100), xlabel='Age (years)', ylabel='Net Worth', axis_center=(age_0, 0))