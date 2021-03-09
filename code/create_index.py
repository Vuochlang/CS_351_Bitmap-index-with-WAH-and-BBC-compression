import os
import math


def convert_to_index(iter_parts):
    parts = iter_parts.split(',')
    parts[2] = parts[2][:-1]
    string = ""
    animal = {
        "cat": "1000",
        "dog": "0100",
        "turtle": "0010",
        "bird": "0001"
    }
    age = {
        1: "1000000000",
        2: "0100000000",
        3: "0010000000",
        4: "0001000000",
        5: "0000100000",
        6: "0000010000",
        7: "0000001000",
        8: "0000000100",
        9: "0000000010",
        10: "0000000001"
    }
    adopted = {
        "True": "10",
        "False": "01"
    }
    string += str(animal.get(parts[0]))
    string += str(age.get(math.ceil(int(parts[1])/10)))
    string += (str(adopted.get(parts[2])) + '\n')
    return string


def convert_and_write_to_file(input_data, output_path_name):
    try:
        fd_output = open(output_path_name, 'w')
    except OSError:
        print(f'cannot create {output_path_name} file to write')
        return()
    else:
        for line in input_data:
            fd_output.write(convert_to_index(line))
        fd_output.close()


def create_index(input_file, output_path, sorted):
    try:
        fd_input = open(input_file, 'r')
    except OSError:
        print(f'cannot open {input_file} to read')
        exit()
    else:
        data = fd_input.readlines()
        if not sorted:
            output_file = os.path.join(output_path, input_file)
            convert_and_write_to_file(data, output_file)

        data.sort()
        output_file = os.path.join(output_path, input_file + "_sorted")
        convert_and_write_to_file(data, output_file)
        fd_input.close()
