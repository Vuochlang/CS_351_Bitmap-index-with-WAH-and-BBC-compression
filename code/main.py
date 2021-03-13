# import create_index as create
# # import compress_index as compress
# # from pathlib import Path
import index_module as im

if __name__ == "__main__":
    file_name = "animals_small.txt"
    # output_path = Path("my_output/bitmaps/")
    im.create_index(file_name, "my_output/bitmaps/", False)

    bitmap_index = "animals_small50.txt"
    # output_path = Path("my_output/compressed")
    im.compress_index(bitmap_index, "my_output/compressed", "WAH", 8)
    # compress.compress_index(bitmap_index, output_path, "BBC", 8)
