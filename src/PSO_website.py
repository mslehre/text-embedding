from os import path

from flask import Flask, render_template, request

from chunks_for_question import get_k_IDs
from ask_question import get_answer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    """This function is called when the user opens the website. It returns the
    website.  

    Returns: 
        str: A string is returned that contains html code for a web form that
            contains text field where the user can ask any question about the 
            examination regulations in the text corpus. If the button 
            'get answer' is pressed, the answer from the LLM is displayed. The
            answer is generated using the best 5 hits from the text corpus 
            chunks. It also displays the text chunks that were used to generate
            the answer.
    """
    answer = 'The answer will be displayed here.'
    question = 'Please enter your question here.'
    if request.method == 'POST':
        question = request.form['question']
        # Call your answer calculation function or logic here
        #answer = get_answer_from_question(question)
        answer = get_answer_from_question(question)
    return render_template("PSO_website.html", answer = answer, 
                           question=question)

def get_answer_from_question(question:str) -> str:
    """This function selects the 5 most similiar chunks for the question and 
    displayes the answer that was given from the LLM based on the chunks.

    Returns: 
        str: A string is returned that contains html code for a web form that
            contains the question and the answer that was generated by the LLM.    
    """
    # Get the question from the 'PSO_website.html' form
    question = request.form['question']

    # Get the 5 best text chunk IDs from the examination regulations chunks 
    # directory
    ids = get_k_IDs(question=question,
                    embeddings_file="../data/examination_regulations.h5")
        
    answer = get_answer(query=question,
                    text_dir="../data/examination_regulations_filtered_chunks/",
                    id_list=ids)

    return answer

if __name__ == '__main__':
    app.run(debug=True)