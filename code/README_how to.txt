There are three two .py files:
1. create_index.py, includes the function
        create_index(input_file, output_path, sorted)
2. compress_index.py, includes the function
        compress_index(bitmap_index, output_path, compression_method, word_size)

To use create_index() in create_index.py:
    _ simply import from create_index.py and call create_index()
    _ example, to use create_index():
        import create_index as c
        if __name__ == "__main__":
            file_name = "animals_small.txt"
            output_path = "path/example"
            c.create_index(file_name, output_path, False)

To use compress_index() in compress_index.py:
    _ simply import from compress_index.py and call compress_index()
    _ the compress_index.py includes:
        1. function: compress_index() for calling compression method on the bitmap_index
                    which will do the WAH or BBC compression as needed
        2. class: WAH class for Word Aligned Hybrid compression
        3. class: BBC class for Bit-aligned Bitmap Compression compression
    _ example, to use compress_index():
        import compress_index as c
        if __name__ == "__main__":
            bitmap_index = "animals_small.txt"
            output_path = "path/example"
            c.compress_index(bitmap_index, output_path, "WAH", 64)
            c.compress_index(bitmap_index, output_path, "BBC", 8)
