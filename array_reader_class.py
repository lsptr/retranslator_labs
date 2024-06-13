import random
import os
import re

class ArrayReader:
    def __init__(self):
        self.commands_dict = ["Load", "Save", "Rand", "Concat", "Free", "Remove", "Copy", "Sort", "Shuffle", "Stats", "Print"]
        self.arrays = {chr(i): [] for i in range(ord('A'), ord('Z') + 1)}

    def parse_command(self, command):
        if command.startswith("Free"):
            parts = command.split('(')
            parts[1] = parts[1].rstrip(')')
            return parts
        else:
            parts = command.split(',')
            first_part_split = parts[0].split(' ')
            new_parts = [first_part_split[0]] + [first_part_split[1]] + parts[1:]
            new_parts = [item.replace(' ', '') for item in new_parts]
            return new_parts
    def execute(self, command):
        parts = self.parse_command(command)
        if parts[0] in self.commands_dict:
            if len(parts) == 1:
                raise StopIteration("Неправильные аргументы операции")
            elif len(parts) == 2:
                if parts[0] == "Free":
                    a = parts[1]
                    self.free_op(a)
                elif (parts[0] == "Sort") and (parts[1][1] == "+"):
                    a = parts[1][0]
                    self.sort_plus_op(a)
                elif (parts[0] == "Sort") and (parts[1][1] == "-"):
                    a = parts[1][0]
                    self.sort_minus_op(a)
                elif (parts[0] == "Shuffle"):
                    a = parts[1]
                    self.shuffle_op(a)
                elif (parts[0] == "Stats"):
                    a = parts[1]
                    self.stats_op(a)
                else:
                    raise StopIteration("Неправильное количество аргументов - 1")
            elif len(parts) == 3:
                if parts[0] == "Load":
                    a = parts[1]
                    file_in = parts[2]
                    self.load_op(a, file_in)
                elif parts[0] == "Save":
                    a = parts[1]
                    file_out = parts[2]
                    self.save_op(a, file_out)
                elif parts[0] == "Concat":
                    a = parts[1]
                    b = parts[2]
                    self.concat_op(a, b)
                elif (parts[0] == "Print") and (parts[2] == "all"):
                    a = parts[1]
                    self.print_all_op(a)
                elif (parts[0] == "Print") and (parts[2].isdigit()):
                    a = parts[1]
                    pos = int(parts[2])
                    self.print_pos_op(a, pos)
                else:
                    raise StopIteration("Неправильное количество аргументов - 2")
            elif len(parts) == 4:
                if parts[0] == "Remove":
                    a = parts[1]
                    index = int(parts[2])
                    num = int(parts[3])
                    self.remove_op(a, index, num)
                elif parts[0] == "Print":
                    a = parts[1]
                    index_start = int(parts[2])
                    index_end = int(parts[3])
                    self.print_range_op(a, index_start, index_end)
                else:
                    raise StopIteration("Неправильное количество аргументов - 3")
            elif len(parts) == 5:
                if parts[0] == "Rand":
                    a = parts[1]
                    count = int(parts[2])
                    lb = int(parts[3])
                    rb = int(parts[4])
                    self.rand_op(a, count, lb, rb)
                elif parts[0] == "Copy":
                    a = parts[1]
                    index_start = int(parts[2])
                    index_end = int(parts[3])
                    b = parts[4]
                    self.copy_op(a, index_start, index_end, b)
                else:
                    raise StopIteration("Неправильное количество аргументов - 4")
        else:
            raise StopIteration("Неизвестная команда")

    def load_op(self, array_name, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines:
                    values = []
                    for line in lines:
                        stripped_line = line.strip()
                        if stripped_line:
                            try:
                                numbers = re.findall(r'\d+', stripped_line)
                                values.extend(map(int, numbers))
                            except ValueError:
                                pass
                    self.arrays[array_name] = values
                else:
                    print("Empty file!")
        else:
            print("File does not exist!")

    def save_op(self, array_name, file_path):
        if os.path.exists(file_path):
            values = self.arrays[array_name]
            with open(file_path, 'w') as file:
                for value in values:
                    file.write(f"{value}\n")
        else:
            print("File does not exist!")

    def rand_op(self, array_name, count, lb, rb):
        if lb >= rb:
            print("Range error!")
        if count > rb - lb:
            print(f"Cannot generate {count} unique numbers within the range [{lb}, {rb}]")
            return
        else:
            self.arrays[array_name] = random.sample(range(lb, rb), count)

    def concat_op(self, a, b):
        self.arrays[a] += self.arrays[b]

    def free_op(self, array_name):
        self.arrays[array_name] = []

    def remove_op(self, array_name, index, num):
        if index < len(self.arrays[array_name]):
            # Проверяем, не превышает ли заданное количество удаления длину массива
            actual_num_to_remove = min(num, len(self.arrays[array_name]) - index)
            del self.arrays[array_name][index:index + actual_num_to_remove]
        else:
            print(f"Index {index} is out of bounds for array {array_name}")

    def copy_op(self, a, start_index, end_index, b):
        if start_index >= len(self.arrays[a]) or end_index >= len(self.arrays[a]) or start_index > end_index:
            print(
                f"Invalid range for copying elements from array {a}. Start index: {start_index}, End index: {end_index}")
            return
        self.arrays[b] = self.arrays[a][start_index:end_index + 1]

    def sort_plus_op(self, array_name):
        self.arrays[array_name].sort()

    def sort_minus_op(self, array_name):
        self.arrays[array_name].sort(reverse=True)

    def shuffle_op(self, array_name):
        random.shuffle(self.arrays[array_name])

    def stats_op(self, array_name):
        size = len(self.arrays[array_name])
        max_val = max(self.arrays[array_name])
        min_val = min(self.arrays[array_name])
        avg_val = sum(self.arrays[array_name]) / size
        variance = sum((x - avg_val) ** 2 for x in self.arrays[array_name]) / size
        std_dev = variance ** 0.5
        mode_val = max(set(self.arrays[array_name]), key=self.arrays[array_name].count)
        print(f"Size: {size}, Max: {max_val}, Min: {min_val}, Most frequent: {mode_val}, Avg: {avg_val}, Variation: {std_dev}")

    def print_all_op(self, array_name):
        print(*self.arrays[array_name], sep='\n')

    def print_pos_op(self, array_name, position):
        if position < len(self.arrays[array_name]):
            print(self.arrays[array_name][position])
        else:
            print(f"Position {position} is out of bounds for array {array_name}")

    def print_range_op(self, array_name, start_index, end_index):
        if start_index < len(self.arrays[array_name]) and end_index < len(self.arrays[array_name]) and start_index <= end_index:
            print(*self.arrays[array_name][start_index:end_index + 1], sep='\n')
        else:
            print(
                f"Invalid range for printing elements from array {array_name}. Start index: {start_index}, End index: {end_index}")

