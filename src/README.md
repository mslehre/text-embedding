# Title 
## Web form
It may be necessary to download flask to run the application. 
To provide this type "pip install flask" in a prompt line.
## Test cosine similarity for files
For testing whether two files are predicted to be more similar than other files
you have to create a tab-separated text file in `/data` with 5 columns.
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
