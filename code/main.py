import create_index as create
import compress_index as compress
from pathlib import Path

if __name__ == "__main__":
    file_name = "animals_small.txt"
    output_path = Path("my_output/bitmaps/")
    create.create_index(file_name, output_path, False)

    bitmap_index = "animals_small50.txt"
    output_path = Path("my_output/compressed")
    # compress.compress_index(bitmap_index, output_path, "WAH", 64)
    compress.compress_index(bitmap_index, output_path, "BBC", 8)
