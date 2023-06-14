import os

from compute_embedding import compute_similarity_of_texts

def read_file(filename_in: str, filename_out: str) -> None:
    """This function reads in a file line by line and splits each line into
    a list. Each line shoul be split at the space character.

    Args:

    Returns:
    """
    # The files that the cosine similarity is computed for has to be in 
    # the directory testTextPais_WebForm.
    path_texts = '../data/testTextPairs_WebForm/'
    # Open the file that contains the filenames of the files that the cosine
    # similarity is computed for and read it line by line.
    file = open('../data/' + filename_in, "r")
    lines = file.readlines()
    file.close()

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
            if (similarity_1 == -2.0 or similarity_2 == -2.0):
                with open('../data/' + filename_out, "a") as file_out:
                    file_out.write("The embedding for one of the files in " \
                        "line" + str(i + 1) + " in " + filename_in + " could " \
                        "not be computed. Maybe the openai api key is not " \
                        "valid or was not set as environment variable.\n")
                    file_out.close()
            else:
                if ((similarity_1 < similarity_2) == int(lines[i][4].strip())):
                    with open('../data/' + filename_out, "a") as file_out:
                        file_out.write("The computed similarity for line", i + \
                            1, "in", filename_in, "is", similarity_1, "and " \
                            "the label is", lines[i][4].strip(), ".\n")
                        file_out.close()

def main():
    read_file('testfiles.txt', 'output.txt')
    exit(0)

if __name__ == "__main__":
    main()