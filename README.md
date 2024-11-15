# Retirement Estimator

A fun little project that estimates net worth based on a particular retirement age.

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Run it:
```bash
python main.py \
  --birthdate 1970-01-01 \
  --net-worth 50_000 \
  --working-income 70_000 \
  --working-spending 30_000 \
  --retirement-age 65 \
  --retired-spending 22_000 \
  --target-date 2025-01-01 \
  --target-worth 100_000
```

It will output:
- The estimated net worth at retirement and the target date (if provided)
- The break-even net worth, at which you could sustain your retirement spending off returns alone
- The estimated age at which the break-even net worth is achieved, and at which the target worth is achieved (if provided)
- A chart showing the estimated net worth over time

Run `-h` for more details and options:
```bash
python main.py -h
```

## History

I created this in 2014 as a (Sage)[https://www.sagemath.org/] script. It was a fun way to experiment with the differential equations behind continuously compounding interest while also planning my own finances. 

In 2020, I ported it to Python and added features around back-calculating age from a target net worth.

In 2024, I removed personal data and open sourced it.