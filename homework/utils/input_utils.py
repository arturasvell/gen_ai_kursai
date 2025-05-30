def expect_for_valid_integer_input(min_number:int):
    arg = ""
    while len(str(arg)) == 0:
        print("Please input a valid integer")
        arg = input()
        try:
            arg = int(arg)
        except ValueError as e:
            print(f"Failed to convert {arg} to int. Please try again")
            arg = ""
        
        if arg < min_number:
            print(f"Provided number {arg} was smaller than expected {min_number}. Please try again.")
            arg = ""
    return int(arg)

def expect_for_valid_float_input(min_number:float):
    arg = ""
    while len(str(arg)) == 0:
        print("Please input a valid integer")
        arg = input()
        try:
            arg = float(arg)
        except ValueError as e:
            print(f"Failed to convert {arg} to float. Please try again")
            arg = ""
        
        if arg < min_number:
            print(f"Provided number {arg} was smaller than expected {min_number}. Please try again.")
            arg = ""
    return float(arg)

def is_int(arg)->bool:
    if type(arg) is int:
        return True
    return False