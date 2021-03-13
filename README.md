# CS 351 - Introduction to Database System       

<h1> Assignment: <br>Bitmap indexing with WAH and BBC compression</h1>

03/12/2021

<h2> Instruction: </h2>

<p>"Creating a bitmap index from a data file containing information about pets and whether they are adopted or not. 
Once create the bitmap, it needs to be compressed using WAH or BBC."</p>

<h3> Program Interface (Required) </h3>

<h4> create_index(input_file, output_path, sorted) </h4>
<h4> compress_index(bitmap_index, output_path, compression_method, word_size) </h4>

<h5> Requirements: </h5>
    _ Do not use any libraries for bitmap creation or compression 
    _ Design of WAH should be independent of word size, example, 8, 16, 32, 62, etc.
