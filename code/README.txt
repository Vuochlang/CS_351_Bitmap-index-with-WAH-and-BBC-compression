There are three .py files:
1. create_index.py, includes the function
        create_index(input_file, output_path, sorted)
2. compress_index.py, includes the function
        compress_index(bitmap_index, output_path, compression_method, word_size)
3. index_module.py, will be the module to import to call create_index() and compress_index()
        from above two files

To use create_index() and compress_index():
    _ simply import from index_module.py and call create_index() or compress_index()
    _ example:
        import index_module as im
            file_name = "animals_small.txt"
            output_path = "path/example"
            im.create_index(file_name, output_path, False)
            im.compress_index(file_name, output_path, "WAH", 8)
            im.compress_index(file_name, output_path, "BBC", 8)