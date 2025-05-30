from utils.input_utils import expect_for_valid_float_input

fahrenheit:int = expect_for_valid_float_input(-60)

celsius:float = (float(fahrenheit) - 32) * 5/9

print(f"The converted C temperature is {celsius}")