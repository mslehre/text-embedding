# Title 

## Web form
It may be necessary to download flask to run the application. 
To provide this type "pip install flask" in a prompt line.

## Test cosine similarity for files
For testing whether two files are predicted to be more similar than other files
you have to create a tab-separated text file in `/data` with $5$ columns.
The first four columns contain the name of the files for which the cosine 
similarity should be computed. The cosine similarity is computed of the first 
two and the third and fourth file. The files for which the cosine similarity 
should be computed have to be stored in `/data/testTextPairs`. The fifth 
column contains a boolean value which is $1$ if you expect the third and 
fourth file to be more similar than the first two files and $0$ otherwise.
The result is written to an output file in `/data`.

Example for an input file:
```
text1.txt	text2.txt	text3.txt	text4.txt	0
text5.txt	text6.txt	text6.txt	text7.txt	1
```
If you just run `test_similarities.py` the input file is `testfiles.txt` in 
`/data` and the output file is `output.txt`. If you want different in- and 
output files you need to call the method `check_cosine_similarity` with your
desired in- and output files.

## Chunker
The chunker takes a list of space separated files, cuts the files into chunks
the number of `chunk_size` characters with overlap of `overlap` characters.
The chunks are saved in files with name `input_file_stem.chunk_index.txt` in
the directory `dir_path`.

An example call is:
```
chunker.py <file1> [<file2> ...] -s <chunk_size> -o <overlap> -d <dir_path>
```
For more information see `chunker.py -h`.

## Compute embeddings for files and save in HDF5-file
The script `txt_to_hdf5.py` has two functions. It can take a directory (`-d`)
containing either text files or subdirectories containing text files as input, 
computes embeddings for every file and saves them and the file IDs in a 
HDF5-file. It can also update (`-u`) the embeddings in an existing HDF5-file,
for that specify a list of files to update the embeddings for or a directory 
containing the text files.

An example call is:
```
txt_to_hdf5.py -d <dir_path> -f <hdf5_file>
``` 

## t-SNE Plot for publication lists
With `tsne_plot.py` the embeddings of publication lists can be visualize with a
 t-SNE plot colored by the chose affiliation (intitute or faculty). For that 
 you need 3 files:
 1. A HDF5-file containing pandas dataframes 
 `embeddings` containing the embeddings of the publication lists and `ids` 
 containing the author IDs corresponding to the embeddings. 
2. A file with a tab-separated table containing author ID, author name, and the
faculty and/or institute of the author.
3. A file containig a tab-separated table of all faculties or institutes.

A bare bones call would be:
```
tsne_plot.py <hdf5_file> <authors_file> <affiliation_file>
```
With optional arguments you can specify the name of the output file, the 
output format, add edges between the most similar authors, or thin out the data 
by number of publications. For further information see `tsne_plot.py -h`.
