from utils.input_utils import expect_for_valid_float_input

celsius:float = expect_for_valid_float_input(-60)

fahrenheit:float = (float(celsius) * 9/5) + 32

print(f"The converted F temperature is {fahrenheit}")