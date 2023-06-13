def prompt(
    query: str,
    chunks: dict,
) -> str:

#key relevant or not? docs will probably all start with the name of the scientist so could leave key out
#left to do: add upper limit for prompt length -> not too many tokens
    context=""
    for key in chunks:
        context+= key + ": " + chunks[key] + "\n"

    template=f"""You are a Bot assistant answering any questions about documents.
You are given a question and a set of documents.
If the user's question requires you to provide specific information from the documents, give your answer based only on the examples provided below. DON'T generate an answer that is NOT written in the provided examples.
If you don't find the answer to the user's question with the examples provided to you below, answer that you didn't find the answer in the documentation and propose him to rephrase his query with more details.
Use bullet points if you have to make a list, only if necessary.

QUESTION: {query}

DOCUMENTS:
=========
{context}
=========
Finish by proposing your help for anything else.
"""

    return template

test_q="a test"
test_chunks={'first': 'this is an apple', 'second': 'this is a banana', 'third': 'this is an orange'}

testp=prompt(test_q, test_chunks)
print(testp)