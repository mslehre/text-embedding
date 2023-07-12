from os import path

from flask import Flask, render_template, request
from openai.embeddings_utils import cosine_similarity, get_embedding

from compute_embedding import embedding_from_string, compute_similarity_of_texts

app = Flask(__name__)
@app.route('/')
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
    return render_template("PSO_website.html")

if __name__ == '__main__':
    app.run(debug=True)
