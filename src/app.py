#to test locally in apphub, switch localhost:5000 to apphub-[username].wolke.uni-greifswald.de/proxy/5000/
from os import path
from flask import Flask, render_template, request
from openai.embeddings_utils import cosine_similarity, get_embedding
from tenacity import RetryError
import pandas as pd
import h5py
import re

from compute_embedding import embedding_from_string, compute_similarity_of_texts
from justify_similarities import ask_about_fit
from chunks_for_question import get_k_IDs
from ask_question import get_answer, get_texts_from_ids
from settings import DATA_DIR

app = Flask(__name__, static_folder = 'static')

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
    if False: # is this needed? remove if not
        profsfile = open(path.join(DATA_DIR, "profs_and_ids.tbl"), "r")
        lines = profsfile.readlines()
        profs ={}
        for line in lines:
            this_line = line.split("\t")
            profs[this_line[0]] = this_line[1]
    return render_template("index.html")


@app.route('/PSO', methods=['GET', 'POST'])
def PSO_home() -> str:
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
                    embeddings_file = "examination_regulations.h5",
                    k = k)

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

@app.route('/simresult', methods=['POST', 'GET'])
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


@app.route('/collab', methods=['GET'])
def show_collabs_page() -> str:
    profsfile = open(path.join(DATA_DIR, "profs_and_ids.tbl"), "r")
    lines = profsfile.readlines()
    profs ={}
    for line in lines:
        this_line = line.split("\t")
        profs[this_line[0]] = this_line[1]
    return render_template("suggestCollabs.html", profs = profs)

@app.route('/collab', methods=['POST'])
def suggest_collabs() -> str:
    profsfile = open(path.join(DATA_DIR, "profs_and_ids.tbl"), "r")
    lines = profsfile.readlines()
    profs ={}
    for line in lines:
        this_line = line.split("\t")
        profs[this_line[0]] = this_line[1]
    
    scientist1 = request.form['scientist1']
    scientist2 = request.form['scientist2']

    collab_suggestion = ask_about_fit([scientist1, scientist2],
                                      path.join(DATA_DIR, "publications"), 2)
    return render_template("suggestCollabs.html", profs= profs,
                           text=collab_suggestion,
                           sel1 = scientist1, sel2 = scientist2)

# navigate to grant call form when button is clicked
@app.route('/grantcall', methods=['POST', 'GET'])
def navigateToGrantCallForm() -> str:
    return render_template("grantCallForm.html")

# calculate similarity and list k most similar scientist upon button click 
@app.route('/grantcallResult', methods=['POST', 'GET'])
def calculateGrantCallResult() -> str:
    # k most similar scientists to display
    k = 10
    # get grant call text
    grantCall = request.form["grantCall"]
    # calculate embedding for grant call text
    try:
        grantCallEmbedding = embedding_from_string(grantCall)
    except RetryError:
        return render_template("displayGrantCallResult.html",
                               text1 = "Please enter a text.")

    # get embeddings from publication list file
    # hdf contains more than one object.
    hdf = pd.HDFStore(path.join(DATA_DIR, "pub_embeddings.h5"), mode='r')
    embeddings = pd.read_hdf(hdf, "embeddings")
    ids = pd.read_hdf(hdf, "ids")
    hdf.close()

    # set k to be smaller, if number of ids is small
    if ids.shape[0] < k:
        k = ids.shape[0]
    
    similarityList = []
    for j in range(0, len(ids)-1):
        # get associated embedding
        embedding = embeddings.iloc[j]
        try:
            similarity = cosine_similarity(grantCallEmbedding, embedding)
        except ValueError:
            return render_template("displayGrantCallResult.html",
                                   text1 = "Please enter a text.")
        similarityList.append((similarity, int(ids.iat[j, 0])))
    # sort list by similarity
    similarityList = sorted(similarityList, reverse = True)
    
    # output k most similar
    outputText = ""
    # get names
    prof_df = pd.read_table(path.join(DATA_DIR, "prof.tbl"))
    # if number of ids is too small, set k to be smaller
    num_id = prof_df["id"].shape[0]
    if num_id < k:
        k = num_id
    for i in range(k):
        firstname = prof_df.loc[prof_df.id == similarityList[i][1],
                                "firstname"].values[0]
        lastname = prof_df.loc[prof_df.id == similarityList[i][1],
                                "lastname"].values[0]
        entry = ("<pre>" + str(firstname) + " " + str(lastname)
                 + "    " + str(similarityList[i][0]) + "</pre>" + "<br>")
        outputText += entry
    return render_template("displayGrantCallResult.html", text1 = outputText)

if __name__ == '__main__':
    app.run(debug=True)
