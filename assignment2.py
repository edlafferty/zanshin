# Assignment 2

name_list = ["Ed", "Bonnie", "Ian", "Maggie", "Heather", "Shadow", "Mittens", "Murphy", "Nero"]

def name_length(name):
    return len(name)

for name_element in range(len(name_list)):
    name = name_list[name_element]
    if name_length(name) > 5:
        print("Name #", name_element+1, "is", name, "and it is", name_length(name), "characters long.")
    if ("n" in name) or ("N" in name):
        print("Name #", name_element+1, ",", name,", contains an \"n/N\".")
print("Let's empty the list, shall we?")
while len(name_list) > 0:
    popped_name = name_list.pop()
    print("POP!  Name:", popped_name, "was removed from the list.")
else:
    print("The name list is empty.  :-(")