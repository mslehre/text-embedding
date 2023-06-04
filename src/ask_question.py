#Questions to work through:
# - settings (temperature etc) correct for us?
# - add testing function? need example vectors for this...

#set key with export OPENAI_API_KEY="..."
import os

import langchain
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
from langchain import VectorDBQA
from langchain import PromptTemplate

from compute_embedding import embedding_from_string

# [Prompt]
this_prompt_template = """You are a Bot assistant answering any questions about documents.
You are given a question and a set of documents.
If the user's question requires you to provide specific information from the documents, give your answer based only on the examples provided below. DON'T generate an answer that is NOT written in the provided examples.
If you don't find the answer to the user's question with the examples provided to you below, answer that you didn't find the answer in the documentation and propose him to rephrase his query with more details.
Use bullet points if you have to make a list, only if necessary.

QUESTION: {question}

DOCUMENTS:
=========
{context}
=========
Finish by proposing your help for anything else.
"""

def answer(
  prompt: str, 
  persist_directory: str
  ) -> str:
        """From a question asked by the user, generate the answer based on the vectorstore.

        Args:
            prompt (str): Question asked by the user.
            persist_directory (str): Vectorstore directory.

        Returns:
            str: Answer generated with the LLM
        """
        #reads in vectorstore:
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embedding_from_string)
        prompt_template = PromptTemplate(template=this_prompt_template, input_variables=["context", "question"])

        #sets settings for LLM:
        doc_chain = load_qa_chain(
            llm=OpenAI(
              model_name="text-davinci-003",
              temperature=0,
              max_tokens=300, # Maximal number of tokens returned by the LLM
            ),
            chain_type="stuff", 
            prompt=prompt_template,
        )

        #calls LLM to ask question
        qa = VectorDBQA(
            vectorstore=vectorstore,
            combine_documents_chain=doc_chain,
            k=4
        )
        result = qa({"query": prompt})
        answer = result["result"]
        return answer