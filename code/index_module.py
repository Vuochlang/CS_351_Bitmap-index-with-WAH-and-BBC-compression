import compress_index as coi
import create_index as ci


def create_index(input_file, output_path, sorted):
    ci.create_index(input_file, output_path, sorted)


def compress_index(bitmap_index, output_path, compression_method, word_size):
    coi.compress_index(bitmap_index, output_path, compression_method, word_size)