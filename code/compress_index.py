import os


class WAH:  # WAH compression class
    def __init__(self, data, word_size):
        self.data = data
        self.size = word_size - 1

    @staticmethod
    def __list_to_string(my_list):  # turn a list to a string
        string = ""
        string = string.join(my_list)
        return string

    def __add_binary(self, list1, list2):  # get two lists and add their value as binary, return the sum as a list
        length = len(list1)
        bin1_str = self.__list_to_string(list1)
        bin2_str = self.__list_to_string(list2)

        total = bin(int(bin1_str, 2) + int(bin2_str, 2))
        total = list(total[2:])

        if len(total) < length:
            dif = length - len(total)
            new_total = ["0"] * dif + total
            return new_total

        return total

    @staticmethod
    def __is_run(chunk):  # check if the given bit string is a run of 0's or 1's
        initial = chunk[0]
        for i in range(1, len(chunk)):
            if chunk[i] != initial:
                return False
        return True

    def __add_run(self, section):  # create a list of run of either 1's or 0's with the 'size'
        compress = ["1"]  # run bit
        compress += str(section[0])  # run of 0 or 1
        compress += (["0"] * (self.size - 2)) + ["1"]
        return compress

    @staticmethod
    def __add_literal(section):
        compress = ["0"]
        compress += [i for i in section]  # append the whole bit string
        return compress

    def compress(self):
        for column in range(16):
            string = ""

            for each_line in self.data:
                string += each_line[column]

            # run through each column
            # divide into list with length of 'size' and compress them
            chunks = [string[i:(i + self.size)] for i in range(0, len(string), self.size)]

            compressed = []
            previous_was_run = False

            for each_section in chunks:

                if len(each_section) < self.size:  # leftover bit < size
                    compressed += self.__add_literal(each_section)
                    compressed += ["0"] * (self.size - len(each_section))  # add the leftover right side with 0's
                    break

                if self.__is_run(each_section):  # a run of either 1 or 0
                    if len(compressed) == 0:  # first run
                        compressed += self.__add_run(each_section)
                        previous_was_run = True
                    else:
                        if previous_was_run:
                            if compressed[-self.size] == each_section[0]:  # same run as previous
                                previous = compressed[-(self.size - 1):]
                                new_value = ["0"] * (self.size - 2) + ["1"]

                                # slice out bits to store number of run
                                compressed = compressed[:(len(compressed) - self.size + 1)]

                                # append new sum binary value
                                compressed += self.__add_binary(previous, new_value)

                            else:  # new run, differ from previous run
                                compressed += self.__add_run(each_section)

                        else:  # previous was literal
                            compressed += self.__add_run(each_section)
                            previous_was_run = True

                else:  # literal
                    compressed += self.__add_literal(each_section)
                    previous_was_run = False

            yield self.__list_to_string(compressed)


def compress_index(bitmap_index, output_path, compression_method, word_size):

    # create the output file name and join with the output_path
    combine_name = bitmap_index + "_" + compression_method + "_" + str(word_size)
    output_file = os.path.join(output_path, combine_name)

    try:  # open the given file to read
        fd_input = open(bitmap_index, 'r')
    except OSError:
        print(f'cannot open {bitmap_index} to read')
        exit()
    else:
        try:  # create a file in the given output_path
            fd_output = open(output_file, 'w')
        except OSError:
            fd_input.close()
            print(f'cannot create {output_file} to write')
            exit()
        else:
            data = fd_input.readlines()
            if compression_method == 'WAH':  # WAH compression
                wah = WAH(data, word_size)
                for each in wah.compress():
                    fd_output.write(each + "\n")
            fd_output.close()
            fd_input.close()
