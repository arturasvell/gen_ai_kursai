import math

def print_various_object_types():
    
    number:int = 1
    
    print(type(number))
    
    bool_example:bool = True
    
    print(type(bool_example))
    
    test_list:list = [1, 2, 3]
    if type(test_list) == list:
        print("%s is of type list" % test_list)
        
    test_tuple:tuple = ("string", 1)
    
    if type(test_tuple) == tuple:
        print("%s is of type tuple" % str(test_tuple))
        
    dictionary:dict ={"test": 1, "test two": 2}
    
    if type(dictionary) == dict:
        print("%s is of type dictionary" % dictionary)
        
    set_example:set = {"one", "two"}
    
    print(type(set_example))
    
def example_sum_method(a:int, b:int) -> int:
    return a+b

def print_example_exception()->None:
    try:
        list_example = [1,2,3]
        
        for element in list_example:
            if element > 1:
                raise Exception("example exception")
    except Exception as e:
        print(e)
        return

def example_math_import_pow(a:int)->int:
    return math.pow(a, 10)

print("Hello World!")
print_various_object_types()
print(example_sum_method(1,2))
print_example_exception()
print(example_math_import_pow(2))