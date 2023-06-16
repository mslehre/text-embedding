#set key with export OPENAI_API_KEY="..."

import os
import openai

from build_prompt import get_prompt

def get_answer(
        query: str, 
        text_dir: str,
        index_list: list) -> str:
    """From a question asked by the user, generate the answer

    Args:
        query (str): Question asked by the user.
        text_dir (str): Documents directory.
        index_list (list): List of relevant docs.

    Returns:
        str: Answer generated with the LLM
    """

    #first read in the chunks given by the index_list from the given directory
    docs = {}
    for i in index_list:
        this_chunk = open(text_dir + "/" + str(i) + ".txt", "r",encoding="UTF-8")
        docs["chunk" + str(i)] = this_chunk.read()
        this_chunk.close()
        
    #assemble the prompt
    this_prompt = get_prompt(query, docs)

    #call openai to obtain a response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=this_prompt,
        temperature=0,
        max_tokens=500,
    )

    result = response['choices'][0]['text']
    return result
    
def test():
    testq = "What are common research interests of these scientists?"
    testdir = "data/example_pubs"
    testlist = [2,4]
    testanswer = get_answer(query=testq,text_dir=testdir,index_list=testlist)
    print(testanswer)