from os import path
import re

from flask import Flask, render_template, request

from chunks_for_question import get_k_IDs
from ask_question import get_answer, get_texts_from_ids
from settings import DATA_DIR

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    """This function is called when the user opens the website. It returns the
    website.  

    Returns: 
        str: A string is returned that contains html code for a web form that
            contains text field where the user can ask any question about the 
            examination regulations in the text corpus. If the button 
            'get answer' is pressed, the answer from the LLM is displayed. The
            answer is generated using the best 4 hits from the text corpus 
            chunks. It also displays the text chunks that were used to generate
            the answer below both: the question and the answer text area.
    """
    answer = ''
    question = ''
    chunk_texts=''
    if request.method == 'POST':
        # Get the question from the form:
        question = request.form['question']
        if question:
            # Get the answer and the texts that were used to asnwer.
            answer, chunk_texts = get_answer_from_question(question, k=4)
        else:
            answer = "Error: Please enter a question."

    return render_template("PSO_website.html", 
                           answer = answer, 
                           question=question, 
                           chunks=chunk_texts)

def get_answer_from_question(question:str,
                             k:int = 4) -> tuple[str,str]:
    """This function selects the k most similiar chunks for the question and 
    returns the answer text as well as a text that contains all used text 
    chunks.

    Args:
        question (str): Question to ask.
        k (int): The number of chunks that are used for answering.

    Returns: 
        str: The asnwer from the LLM.
        str: The texts from the used chunks seperated with some meta 
            information about the corresponding examination regulation.
    """
    # Get the question from the 'PSO_website.html' form
    question = request.form['question']

    # Get the k best text chunk IDs from the examination regulations chunks 
    # directory
    ids = get_k_IDs(question=question,
                    embeddings_file = path.join(DATA_DIR, "examination_regulations.h5"),
                    k=k)
    # Get the asnwer:
    answer = get_answer(query = question,
                text_dir = path.join(DATA_DIR, "examination_regulations_filtered_chunks/"),
                id_list = ids)
    # Format the answer text into a uniform format:
    question = question.strip()
    answer = answer.strip()

    #  delete everything that comes bevor "Answer:" or "answer:" to only get
    # the informative parts from the LLM.
    match = re.search(r'(?i)(?<=Answer:|answer:)\s*(.*)', answer)
    if match:
        answer =  match.group(1).strip() # only the part after "[Aa]nswer:"
    answer = "Question: " + question + "\n\nAnswer: " + answer

    # Get the list of chunk texts:
    chunk_texts_list,_ = get_texts_from_ids(id_list = ids,
                text_dir = path.join(DATA_DIR, "examination_regulations_filtered_chunks/"))
    # Get one text from the chunk texts list 
    chunk_text = ''
    i = 1
    for chunk in chunk_texts_list:
        chunk_text += "\n\n--------------------------------------------------"\
            + "--------------------------------------------------------------"\
            + "-------------------------------\n\n"
        chunk_text += "This is text number " + str(i) + ":\n\n"
        chunk_text += "--------------------------------------------------"\
            + "--------------------------------------------------------------"\
            + "-------------------------------\n\n"
        chunk_text += chunk
        i += 1

    return answer, chunk_text

if __name__ == '__main__':
    app.run(debug=True)
