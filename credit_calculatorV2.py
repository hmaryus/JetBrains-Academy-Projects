import argparse
from math import ceil, log, floor

# Initialize the parser
parser = argparse.ArgumentParser()

# Add the parameters
parser.add_argument('--type', nargs='?')
parser.add_argument('--payment', nargs='?', type=int)
parser.add_argument('--principal', nargs='?', type=int)
parser.add_argument('--periods', nargs='?', type=int)
parser.add_argument('--interest', nargs='?', type=float)

# Parse the arguments
args = parser.parse_args()

# Testing if < 4 arguments
max_args = len(vars(args))
for key,value in vars(args).items():
    if value is None:
        max_args -= 1


if args.type not in ['annuity', 'diff'] or max_args < 4\
            or any(0 > arg for arg in [int(1 if j is None else j) for j in [args.payment, args.principal, args.periods, args.interest]]):
    print('Incorrect parameters')
    exit()

i = (args.interest / 100) / 12  # Interest
P = args.principal              # Credit principal
n = args.periods                # Periods
m = args.payment                # Monthly payment


if args.type == 'diff':
    if args.payment is not None:
        print('Incorrect parameters')

    else:
        total = 0
        for month in range(1, n + 1):
            result = ceil((P / n) + i * (P - ((P * (month - 1)) / n)))
            total += result
            print(f'Month {month}: payment is {result}')

        print(f'\nOverpayment = {total - P}')

if args.type == 'annuity':
    if not args.principal and args.payment:
        result = floor((m / ((i*(1+i)**n) / ((1+i)**n - 1))))
        print(f'Your loan principal = {result}!\nOverpayment = {round(m*n - result)}')

    elif args.principal and args.payment:
        result = ceil(log(m / (m - i * P), 1+i))
        print(
            f'It will take {round(result // 12) if result > 12 else ""}{" years" if result >= 24 else ""}{" year" if 24 > result >= 12 else ""}'
            f' {"and" if ceil(result % 12) > 1 else "to repay this loan!"} {ceil(result%12) if ceil(result%12)>1 else ""}'
            f' {"months to repay this loan!" if ceil(result%12)>1 else ""}\nOverpayment = {round((result-P/m) * m)}')

    else:
        result = ceil(P * ((i * (1+i)**n) / ((1+i)**n - 1)))
        print(f'Your loan principal = {result}!\nOverpayment = {result}')