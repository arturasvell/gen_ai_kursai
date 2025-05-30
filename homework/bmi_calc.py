from utils.input_utils import expect_for_valid_float_input

# categories: Underweight (less than 18.5), Healthy Weight (18.5 to 24.9), Overweight (25 to 29.9), and Obese (30 or more)

print("Input weight in kg")
weight:float = expect_for_valid_float_input(0)

print("Input height in m")
height:float = expect_for_valid_float_input(0)

bmi = weight / (height ** 2)

category = None

if bmi < 18.5:
    category = "Underweight"
elif bmi >= 18.5 and bmi<25:
    category = "Healthy"
elif bmi >=25 and bmi <30:
    category = "Overweight"
elif bmi >= 30:
    category = "Obese"

print(f"Your BMI is {bmi}, you are {category}")