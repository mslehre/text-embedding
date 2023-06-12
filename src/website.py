from os import path

from flask import Flask
from openai.embeddings_utils import cosine_similarity

from compute_embedding import embedding_from_string, compute_similarity_of_texts

app = Flask(__name__)

@app.route('/')
def home():
    return '''<form>
    <label for="fname">Enter first file text: </label><br>
  <textarea name="file1" id="file1text" rows="10" cols="30"></textarea>
  </form>
  
  <form>
  <label for="lname">Enter second file text:</label><br>
  <textarea name="file1" id="file2text" rows="10" cols="30"></textarea>
  </form>

    <button onclick="myFunction()"> Compute similarity of the files content\
        </button> <br><br>

    <p id="demo"> </p>
    <p id="url"> </p>

    <script>
        function myFunction() {
            let f1 = document.getElementById("file1text").value;
            let f2 = document.getElementById("file2text").value;
            let actualUrl = window.location.href;

            document.getElementById("url").innerHTML="";

            if(!f1 || !f2){
                document.getElementById("demo").innerHTML="";
                alert("The file name can not be empty!");
            } else {
                document.getElementById("file1a2").value=f1+f2;
                window.open(actualUrl+"/file1/file2");
            }
        }
    </script>

    <form>
    <textarea name="file1" id=file1a2 rows="10" cols="30">
    </textarea>

    </form>'''

@app.route('/file1/file2') 
def compute_similarity_of_files(text1: str, text2: str) -> str:
    """This function computes the cosine similarity of two embeddings of the 
    specified two texts. If a text is too large because its string is encoded 
    to more tokens than the maximum number of tokens for which an embedding is 
    computed, the embedding for the string that is encoded to the first 
    max_token tokens is computed where max_token is the maximum number of 
    tokens for which an embedding is computed. The cosine similarity is 
    returned as string in a web form. 

    Args:
        text1 (str): This parameter is the string of some sort of text e. g. 
            the content of a file for which the cosine similarity with the 
            string of another text is computed.
        text2 (str): This parameter is the second string of some sort of text 
            e. g. the content of a file for which the cosine similarity with 
            the string of another text is computed.

    Returns: 
        str: A string is returned that contains html code for a web form that
            contains two labels text1 and text2 and the names of the texts the 
            user specified. In a textfield the cosine similarity of the two 
            texts is displayed. If the embedding for one of the texts cannot be 
            computed, there is a message that the openai api key was probably 
            not set or is not valid.     
    """
    # Compute cosine similarity of texts.
    similarity = compute_similarity_of_texts(text1, text2)
        
    text = ""
    # Test if embeddings and cosine similarity could be computed.
    if (similarity == -2.0):
        text += "For at least one of your inserted texts no embedding " + \
                "could be computed. Probably, the openai api key is not " + \
                "valid or set as an environment variable. Therefore, the " + \
                "similarity of the texts cannot be computed."
    else: 
        # Display cosine similarity since embeddings could be computed.
        similarity = cosine_similarity(embeddings[0], embeddings[1])
        text += "The cosine similarity of the two texts you inserted is " + \
            str(similarity) + "."
    return '''
          <label id="file1">file1: '''+text1+'''</label> <br>
          <label id="file2">file2: '''+text2+'''</label> <br>
  
          <form>
          <textarea id="file1content" name="file1" rows="10" cols="30">'''\
              +text+'''</textarea>

          </form>'''

if __name__ == '__main__':
    app.run()

