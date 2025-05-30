from datetime import datetime, date
from math import ceil

def is_int(arg)->bool:
    if type(arg) is int:
        return True
    return False
        
def expect_for_valid_integer_input(min_number:int):
    date = ""
    while len(str(date)) == 0:
        print("Please input a valid integer")
        date = input()
        try:
            date = int(date)
        except ValueError as e:
            print(f"Failed to convert {date} to int. Please try again")
            date = ""
        
        if date < min_number:
            print(f"Provided number {date} was smaller than expected {min_number}. Please try again.")
            date = ""
    return int(date)
        

def ask_for_input()->date:
    birth_year:int = expect_for_valid_integer_input(2000)
    birth_month:int = expect_for_valid_integer_input(7)
    birth_day:int = expect_for_valid_integer_input(1)
    return date(birth_year, birth_month, birth_day)
    
    

now:datetime = datetime.now()
year:int = now.year
month:int = now.month
day:int = now.day
date_of_birth:date = ask_for_input()
print(f"Your birth date is {date_of_birth.year}-{date_of_birth.month}-{date_of_birth.day}")

age_total = date(year, month, day) - date_of_birth
age_years = ceil(age_total.days/365)
print(f"You are {age_years} years old")

if age_years >=0 and age_years<=17:
    print("category I")
if age_years >=18 and age_years<=36:
    print("category II")
if age_years >=37 and age_years<=60:
    print("category III")