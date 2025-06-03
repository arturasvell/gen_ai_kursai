from utils.input_utils import expect_for_valid_float_input
print("Enter five numbers")
num_list = []
for i in range(0,5):
    input_num = expect_for_valid_float_input(-9999)
    num_list.append(input_num)

sum = 0
for num in num_list:
    sum+=num

print(sum/len(num_list))