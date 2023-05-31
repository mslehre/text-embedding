#took example code from article
#Questions to work through:
# - settings (temperature etc) correct for us?
# - add in our embedding etc. functions where needed
# - what should be set as system variable, what hardcoded etc (e.g. vectorstore directory)
# - import needed packages from langchain
# - add main for testing

# [Prompt]
prompt_template = """You are a Bot assistant answering any questions about documents.
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
  self, 
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
        LOGGER.info(f"Start answering based on prompt: {prompt}.")
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        prompt_template = PromptTemplate(template=config.prompt_template, input_variables=["context", "question"])
        doc_chain = load_qa_chain(
            llm=OpenAI(
              openai_api_key=open_ai_key, # set as system variable
              model_name="text-davinci-003",
              temperature=0,
              max_tokens=300, # Maximal number of tokens returned by the LLM
            )
            chain_type="stuff", 
            prompt=prompt_template,
        )
        LOGGER.info(f"The top {config.k} chunks are considered to answer the user's query.")
        qa = VectorDBQA(
            vectorstore=vectorstore,
            combine_documents_chain=doc_chain,
            k=4
        )
        result = qa({"query": prompt})
        answer = result["result"]
        LOGGER.info(f"The returned answer is: {answer}")
        LOGGER.info(f"Answering module over.")
        return answer