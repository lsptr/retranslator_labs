from array_reader_class import ArrayReader

interpreter = ArrayReader()
print(interpreter.commands_dict)
while True:
    try:
        command = input(": ")
        if command == "exit":
            break
        else:
            interpreter.execute(command)
            print(interpreter.arrays)
    except StopIteration as e:
        print(e)
        continue
