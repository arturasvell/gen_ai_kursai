from statistics import mean

item_list = input("Enter item prices separated by commas: ")
split_items = str.split(item_list, ',')

parsed_floats = []
for item in split_items:
    item = item.strip()
    try:
        parsed_floats.append(float(item))
    except ValueError:
        print(f"Warning: '{item}' is not a valid float and will be skipped.")

print("Parsed floats:", parsed_floats)

print("Count of items with price more than 10: %s" % sum(1 for x in parsed_floats if x > 10))
print("Average: %s" % mean(parsed_floats))
print("Sum: %s" % sum(parsed_floats))
print("Count: %s" % len(parsed_floats))