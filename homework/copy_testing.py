from copy import deepcopy
test_list:list[list[int]] = [[1,2,3], [4,5,6]]
print("Original list %s" % test_list)

copy_list:list[list[int]] = test_list.copy() # [[1,2,3], [4,5,6]]
deep_list_copy:list[list[int]] = deepcopy(test_list)

copy_list[0][0] = 100000 # test_list also should change
copy_list.append([7,8,9]) # only copy_list gets new values

print("Test list after changes: %s" % test_list)
print("Shallow copy list %s" % copy_list)
print("Deep copy list %s" % deep_list_copy)