import os


def list_to_string(my_list):  # turn a list to a string
    string = ""
    string = string.join(my_list)
    return string


class WAH:  # Word Aligned Hybrid compression class
    def __init__(self, data, word_size):
        self.data = data
        self.size = word_size - 1
        self.run = 0
        self.literal = 0

    @staticmethod
    def __add_binary(list1, list2):  # get two lists and add their value as binary, return the sum as a list
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
                    self.run += 1
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
                    self.literal += 1
                    compressed += self.__add_literal(each_section)
                    previous_was_run = False

            yield list_to_string(compressed)

        # number of run and literal for the entire file
        # print("# run = " + str(self.run) + ", # literal = " + str(self. literal))


class BBC:  # Byte-aligned Bitmap Compression Class
    def __init__(self):
        self.number_of_run = 0
        self.number_of_literal = 0
        self.literal_list = []

    def reset(self):
        self.number_of_run = 0
        self.number_of_literal = 0
        self.literal_list = []

    @staticmethod
    def __is_run(chunk):  # check if the given bit string is a run of 0's
        for i in range(0, len(chunk)):
            if chunk[i] != "0":
                return False
        return True

    @staticmethod
    def decimal_to_binary(number):  # convert decimal to binary
        bin_list = []
        while number > 0:
            bin_list += [str(number % 2)]
            number //= 2
        bin_list.reverse()
        return bin_list

    @staticmethod
    def __is_special_literal(chunk):  # expecting a non-run bit string (mixture of 0 and 1)
        dirty_bit = 0
        location = 0
        for i in range(0, len(chunk[0])):
            if chunk[0][i] == "1":
                if dirty_bit == 1:
                    return False
                dirty_bit += 1
                location = i + 1  ###################################################
        return location

    def compress(self, data):  # WAH compression on data's columns
        for column in range(16):
            string = ""

            # combine each column per row into a string
            for each_line in data:
                string += each_line[column]

            # divide the string into list with length of 8 bits for BBC to compress them
            chunks = [string[i:(i + 8)] for i in range(0, len(string), 8)]

            found_chunk = False
            last_piece = False
            compressed = []  # store the result of BBC compression
            self.reset()

            # loop through 8 bit at a time to decide what to do
            # set number of literal, run and list of literal as needed
            while len(chunks) > 0:
                each_byte = chunks[0]  # first item in the list

                # check if that 8bit is run or literal
                run = self.__is_run(each_byte)

                if run:

                    # first run in a chunk
                    if not found_chunk and self.number_of_literal == 0:
                        self.number_of_run += 1
                        chunks = chunks[1:]
                        if len(chunks) == 0:
                            last_piece = True

                    # end of current chunk
                    elif not found_chunk and self.number_of_literal > 0:
                        found_chunk = True

                else:  # literal

                    # literal of the chunk
                    if not found_chunk:
                        self.number_of_literal += 1
                        self.literal_list += [each_byte]
                        chunks = chunks[1:]
                        if len(chunks) == 0:
                            last_piece = True

                # when a chunk is found, call compress_chunk() to compress and store result
                if found_chunk:
                    compressed += self.compress_chunk()
                    found_chunk = False
                    self.reset()

                # compress the left over byte
                if last_piece:
                    compressed += self.compress_chunk()
                    break

            yield list_to_string(compressed)

    def compress_chunk(self):  # compress one chunk and return result as a list
        this_list = []
        run_byte = False
        special_literal = False

        # Header bit 1 - 3
        if self.number_of_run > 0:
            if self.number_of_run <= 6:
                this_list += self.add_zero_with_binary(self.number_of_run, 3)
            else:  # run > 6
                run_byte = True
                this_list += ["1"] * 3

        else:  # no run of 0's in the chunk
            this_list += ["0"] * 3

        # Header bit 4, special literal or not
        if self.number_of_literal > 1 or self.number_of_literal == 0:
            this_list += ["0"]

        elif self.number_of_literal == 1:
            special_literal = self.__is_special_literal(self.literal_list)
            if not special_literal:
                this_list += ["0"]
            else:
                this_list += ["1"]

        # Header bit 5 - 8
        if this_list[-1] == "1":  # if bit 4 is special, store the position of the dirty bit
            this_list += self.add_zero_with_binary(special_literal, 4)

        elif this_list[-1] == "0":  # if bit 4 is not special, store number of literals
            this_list += self.add_zero_with_binary(self.number_of_literal, 4)

        # Run byte
        if run_byte:  # if number of run is greater than 6, convert into binary and store in as a byte
            this_list += self.add_zero_with_binary(self.number_of_run, 8)

        # Literal byte
        if not special_literal:  # when bit 4 is "0", store those literal bytes
            for each_literal in self.literal_list:
                this_list += each_literal

        return this_list

    # take in a decimal, convert into binary
    # if the binary bit is less than size, append 0's in front of it
    def add_zero_with_binary(self, decimal, size):
        temp = self.decimal_to_binary(decimal)
        if len(temp) == size:
            return temp
        else:
            return ["0"] * (size - len(temp)) + temp


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
            elif compression_method == 'BBC':  # BBC compression
                bbc = BBC()
                for each in bbc.compress(data):
                    fd_output.write(each + "\n")
            fd_output.close()
            fd_input.close()
