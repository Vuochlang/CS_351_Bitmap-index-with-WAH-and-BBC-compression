import os


def list_to_string(my_list):
    string = ""
    string = string.join(my_list)
    return string


def add_binary(list1, list2):
    length = len(list1)
    bin1_str = list_to_string(list1)
    bin2_str = list_to_string(list2)

    total = bin(int(bin1_str, 2) + int(bin2_str, 2))
    total = list(total[2:])

    if len(total) < length:
        dif = length - len(total)
        new_total = ["0"] * dif + total
        return new_total

    return total


def is_run(chunk):
    initial = chunk[0]
    for i in range(1, len(chunk)):
        if chunk[i] != initial:
            return False
    return True


def add_run(section, size):
    compress = ["1"]  # run bit
    compress += str(section[0])  # run of 0 or 1
    compress += (["0"] * (size - 2)) + ["1"]
    return compress


# def split_data(input_data, word_size):
    # size = word_size - 1
    # for column in range(16):
    #     string = ""
    #
    #     for each_line in input_data:
    #         string += each_line[column]
    #
    #     chunks = [string[i:(i + size)] for i in range(0, len(string), size)]
    #
    #     compressed = []
    #     previous_was_run = False
    #     for each_section in chunks:
    #
    #         if len(each_section) < size:  # leftover bit < size
    #             compressed += ["0"]
    #             compressed += [i for i in each_section]
    #             compressed += ["0"] * (size - len(each_section))
    #             break
    #
    #         if is_run(each_section):  # a run of either 1 or 0
    #             if len(compressed) == 0:  # first run
    #                 compressed += add_run(each_section, size)
    #                 previous_was_run = True
    #             else:
    #                 if previous_was_run:
    #                     if compressed[-size] == each_section[0]:  # same run as previous
    #                         previous = compressed[-(size - 1):]
    #                         new_value = ["0"] * (size - 2) + ["1"]
    #                         compressed = compressed[:(len(compressed) - size + 1)]  # slice out
    #                         compressed += add_binary(previous, new_value)  # append new sum binary value
    #                     else:  # new run, differ from previous run
    #                         compressed += add_run(each_section, size)
    #                 else:  # previous was literal
    #                     compressed += add_run(each_section, size)
    #                     previous_was_run = True
    #
    #         else:  # literal
    #             compressed += ["0"]
    #             compressed += [i for i in each_section]
    #             previous_was_run = False
    #
    #     my_string = list_to_string(compressed)
    #     yield my_string


def compress_wah(input_data, word_size):
    # for i in split_data(input_data, word_size):
    #     yield i
    size = word_size - 1
    for column in range(16):
        string = ""

        for each_line in input_data:
            string += each_line[column]

        chunks = [string[i:(i + size)] for i in range(0, len(string), size)]

        compressed = []
        previous_was_run = False
        for each_section in chunks:

            if len(each_section) < size:  # leftover bit < size
                compressed += ["0"]
                compressed += [i for i in each_section]
                compressed += ["0"] * (size - len(each_section))
                break

            if is_run(each_section):  # a run of either 1 or 0
                if len(compressed) == 0:  # first run
                    compressed += add_run(each_section, size)
                    previous_was_run = True
                else:
                    if previous_was_run:
                        if compressed[-size] == each_section[0]:  # same run as previous
                            previous = compressed[-(size - 1):]
                            new_value = ["0"] * (size - 2) + ["1"]
                            compressed = compressed[:(len(compressed) - size + 1)]  # slice out
                            compressed += add_binary(previous, new_value)  # append new sum binary value
                        else:  # new run, differ from previous run
                            compressed += add_run(each_section, size)
                    else:  # previous was literal
                        compressed += add_run(each_section, size)
                        previous_was_run = True

            else:  # literal
                compressed += ["0"]
                compressed += [i for i in each_section]
                previous_was_run = False

        my_string = list_to_string(compressed)
        yield my_string


def compress_index(bitmap_index, output_path, compression_method, word_size):
    combine_name = bitmap_index + "_" + compression_method + "_" + str(word_size)
    output_file = os.path.join(output_path, combine_name)

    try:
        fd_input = open(bitmap_index, 'r')
    except OSError:
        print(f'cannot open {bitmap_index} to read')
        exit()
    else:
        try:
            fd_output = open(output_file, 'w')
        except OSError:
            fd_input.close()
            print(f'cannot create {output_file} to write')
            exit()
        else:
            data = fd_input.readlines()
            if compression_method == 'WAH':
                wah_index = compress_wah(data, word_size)  # WAH
                for each in wah_index:
                    fd_output.write(each + "\n")
            fd_output.close()
            fd_input.close()
