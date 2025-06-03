groceries = []

while True:
    new_item = input("Input new item to add to the grocery list: ")
    
    if new_item.lower() == "done":
        break
    
    groceries.append(str(new_item))

print(groceries)
print(len(groceries))