#set key with export OPENAI_API_KEY="..."

import os
import openai

from build_prompt import get_prompt

def get_answer(
        query: str, 
        text_dir: str,
        id_list: list[str],
        seperator_list: list[str] = None) -> str:
    """From a question asked by the user, generate the answer

    Args:
        query (str): Question asked by the user.
        text_dir (str): Documents directory.
        id_list (list[str]): List of relevant docs.
        seperator_list (list[str]): List of strings to insert as seperators in
            between the text chunks.

    Returns:
        str: Answer generated with the LLM
    """

    # First read in the chunks given by the id_list from the given directory
    # Either the file exists as it is in the directory or it is located in a 
    # sub directory with the chubks of a larger text file.
    docs = []
    for i in id_list:
        file_path = os.path.join(text_dir, i + ".txt")
        dir_path = os.path.join(text_dir, i.split('.')[0]) # sub dir
        # search for a sub directory with chunks:
        if(not os.path.isfile(file_path) and os.path.isdir(dir_path)):
            file_path = os.path.join(dir_path, i + ".txt")

        if not os.access(file_path, os.R_OK):
            print(f'ERROR: Could not find or acces the file {i}.txt '
                  + f' directly or in a sub directory {dir_path}.')
            exit(1)
                
        this_chunk = open(file_path, "r", encoding="UTF-8")
        docs.append(this_chunk.read())
        this_chunk.close()
        
    #assemble the prompt
    this_prompt = get_prompt(query, docs, seperator_list)
    if (this_prompt == None):
        return None

    #call openai to obtain a response
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = this_prompt,
        temperature = 0,
        max_tokens = 500,
    )

    result = response['choices'][0]['text']
    return result
    
def test():
    testq = "What are common research interests of these scientists?"
    testdir = "data/example_pubs"
    testlist = [2,4]
    testanswer = get_answer(query=testq, text_dir=testdir, id_list=testlist)
    print(testanswer)
