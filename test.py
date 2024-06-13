import re

command = "Print A, bb, c"
if command.startswith("Free"):
    parts = command.split('(')
    parts[1] = parts[1].rstrip(')')
    print(parts)
else:
    parts = command.split(',')
    first_part_split = parts[0].split(' ')
    new_parts = [first_part_split[0]] + [first_part_split[1]] + parts[1:]
    new_parts = [item.replace(' ', '') for item in new_parts]
    print(new_parts)
