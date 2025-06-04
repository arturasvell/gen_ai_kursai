from datetime import datetime, date
from math import ceil

def calculate_age(birth_date:date):
    now:datetime = datetime.now()
    year:int = now.year
    month:int = now.month
    day:int = now.day
    age_total = date(year, month, day) - birth_date
    age_years = ceil(age_total.days/365)
    return age_years

time_str = input("enter time in this format yyyy-mm-dd\n")
time = datetime.strptime(time_str, "%Y-%m-%d")
if time > datetime.now():
    raise Exception("Birth date cannot be in the future")

print("Your age is %s" % calculate_age(time.date()))