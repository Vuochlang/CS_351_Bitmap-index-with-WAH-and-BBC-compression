import create_index as create
import compress_index as compress

if __name__ == "__main__":
    file_name = "animals_small.txt"
    create.create_index(file_name, "my_output/bitmaps/", False)

    bitmap_index = "animals_small2.txt"
    compress.compress_index(bitmap_index, "my_output/compressed", "WAH", 64)
