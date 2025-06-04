from datetime import datetime, date
from utils.input_utils import expect_for_valid_integer_input
from math import ceil

def get_user_birthdate():
    print("Input your birthdate")
    year = expect_for_valid_integer_input(0)
    month = expect_for_valid_integer_input(0)
    day = expect_for_valid_integer_input(0)
    return date(year, month, day)

def calculate_age(birth_date:date):
    now:datetime = datetime.now()
    year:int = now.year
    month:int = now.month
    day:int = now.day
    age_total = date(year, month, day) - birth_date
    age_years = ceil(age_total.days/365)
    return age_years

def get_week_day(date:date):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[date.weekday()]


birth_date = get_user_birthdate()
print("Your birthday is %s" % birth_date)

age = calculate_age(birth_date)
print("Your age is %s" % age)

print("The weekday of your birth date is %s" % get_week_day(birth_date))
    