#Questions to work through:
# - settings (temperature etc) correct for us?
# - add testing function? need example vectors for this...

#example question: What are common interests for these two scientists, give documents: first list, second list....
#set key with export OPENAI_API_KEY="..."

#add argument list of indices, read in eg 1.txt, 5.txt and 7.txt from directory

#first test without that though, make a directory with some testfiles, ask a test question see if it works
#read up and understand what that vectorstore even is and how chroma gets it

#here: https://blog.langchain.dev/langchain-chroma/ and github link in that will help

#https://platform.openai.com/docs/guides/gpt/chat-completions-api
#look up how to most basically ask openai questions, use that


import os
import openai

from build_prompt import prompt


def answer(
  query: str, 
  text_dir: str,
  index_list: list
  ) -> str:
        """From a question asked by the user, generate the answer

        Args:
            query (str): Question asked by the user.
            text_dir (str): Documents directory.
            index_list (list): List of relevant docs.

        Returns:
            str: Answer generated with the LLM
        """

        #first read in docs given by list from the given directory
        docs={}
        for i in index_list:
            this_chunk = open(text_dir + "/" + str(i) + ".txt", "r",encoding="UTF-8")
            docs["chunk" + str(i)]=this_chunk.read()
            this_chunk.close()
        
        #assemble the prompt
        this_prompt=prompt(query, docs)

        #call openai to obtain a response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=this_prompt,
            temperature=0,
            max_tokens=30,
        )

        result = response['choices'][0]['text']
        return result
    
def test():
        testq="Given these lists of favourite foods, what could these two people eat togethers?"
        testdir="/home/fb165560/text-embedding/data/test"
        testlist=[1,3]
        testanswer=answer(query=testq,text_dir=testdir,index_list=testlist)
        print(testanswer)

test()