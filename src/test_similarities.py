import os

from compute_embedding import compute_similarity_of_texts

def check_cosine_similarity(filename_in: str, filename_out: str) -> None:
    """This function reads in a file line by line and splits each line into
    a list. Each line should be split at the space character and should contain
    five strings. The first four strings are filenames of text files which have
    to be stored in /data/testTextPairs_WebForm. The cosine similarity of the
    texts in the first two files and the cosine similarity of the texts in the
    last two files is computed. The similarities of the files are written to
    filename_out. It is tested which cosine similarity is higher or rather the
    content of which of the files is more similar. The result is written to
    filename_out. The fifth string in each line is a boolean value which
    indicates whether the first two files are more similar or the last two
    files. A '1' indicates that the texts of the last two files are more
    similar than the texts of the first two files.  

    Args:
        filename_in (str): This parameter is the name of the file which is read.
            The has to be in the directory /data.
        filename_out (str): This parameter is the name of the file to which the
            results are written. The file is created in the directory /data.

    Returns:
        None: This function does not return a value.
    """
    # The files that the cosine similarity is computed for has to be in 
    # the directory testTextPais_WebForm.
    path_texts = '../data/testTextPairs_WebForm/'
    # Open the file that contains the filenames of the files that the cosine
    # similarity is computed for and read it line by line.
    file = open('../data/' + filename_in, "r")
    lines = file.readlines()
    file.close()
    # Count the number of wrong predictions in filename_in.
    wrong_predictions = 0

    for i in range(0, len(lines)):
        # Split each line at the space character to get the filenames.
        lines[i] = lines[i].split(" ")
        texts = []  # Content of the files is stored in this list.
        for j in range(0, len(lines[i]) - 1):
            lines[i][j] = lines[i][j].strip()
            # Test if a file with the filename specified in the input file 
            # exists. If not write it to the output file and continue with the 
            # next line in the input file.
            if not (os.path.exists(path_texts + lines[i][j])):
                with open('../data/' + filename_out, "a") as file_out:
                    file_out.write("File " + lines[i][j] + " does not exist " \
                        "in text-embedding/data/testTextPairs_WebForm/. " \
                        "Therefore, nothing will be computed for line " + 
                        str(i + 1) + " in " + filename_in + ".\n")
                    file_out.close()
                break
            else:
                # Store the content of the file in the list texts.
                file = open(path_texts + lines[i][j], "r")
                texts.append(file.read())
                file.close()
        if (len(texts) == 4):
            # Compute the cosine similarity of the texts.
            similarity_1 = compute_similarity_of_texts(texts[0], texts[1])
            similarity_2 = compute_similarity_of_texts(texts[2], texts[3])
            # Test if the cosine similarity or rather the embeddings of the 
            # texts could be computed.
            if (similarity_1 == -2.0 or similarity_2 == -2.0):
                with open('../data/' + filename_out, "a") as file_out:
                    file_out.write("The embedding for one of the files in " \
                        "line" + str(i + 1) + " in " + filename_in + " could " \
                        "not be computed. Maybe the openai api key is not " \
                        "valid or was not set as environment variable.\n")
                    file_out.close()
            else:
                # Write the cosine similarities to the output file.
                with open('../data/' + filename_out, "a") as file_out:
                    file_out.write("The cosine similarity of the texts in " 
                        + lines[i][0] + " and " + lines[i][1] + " is " 
                        + str(similarity_1) + " and for the texts in " 
                        + lines[i][2] + " and " + lines[i][3] + " it is "
                        + str(similarity_2) + ". ")
                    file_out.close()

                order_of_texts = [0,2]
                # Test which text pair has the higher cosine similarity this 
                # means the texts are more similar and write the result to the
                # output file.
                if (similarity_1 < similarity_2):
                    order_of_texts = [2, 0]  
                with open('../data/' + filename_out, "a") as file_out:
                    file_out.write("The texts in " + lines[i][order_of_texts[0]]
                        + " and " + lines[i][order_of_texts[0] + 1] + " are " \
                        "more similar than the texts in " 
                        + lines[i][order_of_texts[1]] + " and " 
                        + lines[i][order_of_texts[1] + 1] + ". ")

                prediction_right = ""
                # Test if the prediction in filename_in is right and write the
                # result to the output file.
                if not ((similarity_1 < similarity_2) 
                         == int(lines[i][4].strip())):
                    prediction_right = "not "
                    wrong_predictions += 1
                with open('../data/' + filename_out, "a") as file_out:
                    file_out.write("The result is " + prediction_right 
                        + "as expected.\n")
                    file_out.close()
    with open('../data/' + filename_out, "a") as file_out:
        file_out.write(str(wrong_predictions) + " of " + str(len(lines)) 
            + " predictions are wrong.\n") 
        file_out.close()

def main():
    check_cosine_similarity('testfiles.txt', 'output.txt')
    exit(0)

if __name__ == "__main__":
    main()
