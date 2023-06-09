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
            contains two labels and two textfields. The user can enter two
            texts into the textfields. If the user clicks on the submit button, 
            the texts are sent to the server and the method 'compute_similarity_
            of_texts' is called. The result of this method is returned to the
            user.  
    """
    return render_template("index.html")

@app.route('/result', methods=['POST', 'GET'])
def compute_similarity_of_files() -> str:
    """This function computes the cosine similarity of two embeddings of two 
    texts a user inserted and submitted at the 'index.html' form. If a text is 
    too large because its string is encoded to more tokens than the maximum 
    number of tokens for which an embedding is computed, the embedding for the 
    string that is encoded to the first max_token tokens is computed where 
    max_token is the maximum number of tokens for which an embedding is 
    computed. The cosine similarity is returned as string in a web form. 

    Returns: 
        str: A string is returned that contains html code for a web form that
            contains two labels text1 and text2 and the first 100 words of the texts 
            the user specified. In a textfield the cosine similarity of the two 
            texts is displayed. If the embedding for one of the texts cannot be 
            computed, there is a message that the openai api key was probably 
            not set or is not valid.     
    """
    # Get texts from 'index.html' form
    text1 = request.form['text1']
    text2 = request.form['text2']
    # Compute cosine similarity of texts.
    similarity = compute_similarity_of_texts(text1, text2)
        
    text = ""
    # Test if embeddings and cosine similarity could be computed.
    if (similarity is None):
        text += "For at least one of your inserted texts no embedding " + \
                "could be computed. Probably, the openai api key is not " + \
                "valid or set as an environment variable. Therefore, the " + \
                "similarity of the texts cannot be computed."
    else: 
        # Display cosine similarity since embeddings could be computed.
        text += "The cosine similarity of the two texts you inserted is " + \
            str(similarity) + "."
    texts_start = []
    for string in [text1, text2]:
        words = string.split()[:100]
        texts_start.append(" ".join(words))
    return render_template("displaySimilarity.html", text1=texts_start[0], 
                           text2=texts_start[1], text=text)

if __name__ == '__main__':
    app.run(debug=True)
