from os import path

from flask import Flask
from openai.embeddings_utils import cosine_similarity

from compute_embedding import embedding_from_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''<form>
    <label for="fname">Enter first file name: </label><br>
    <input type="text" id="file1"><br>
    <label for="lname">Enter second file name:</label><br>
    <input type="text" id="file2"><br><br>

    <button onclick="myFunction()"> Compute similarity of the files content\
        </button> <br><br>

    <p id="demo"> </p>
    <p id="url"> </p>

    <script>
        function myFunction() {
            let f1 = document.getElementById("file1").value;
            let f2 = document.getElementById("file2").value;
            let actualUrl = window.location.href;

            document.getElementById("url").innerHTML="";

            if(!f1 || !f2){
                document.getElementById("demo").innerHTML="";
                alert("The file name can not be empty!");
            } else {
                window.open(actualUrl+"/file1/"+f1+"/file2/"+f2);
            }
        }
    </script>

    <form>
    <textarea name="file1" rows="10" cols="30">
    </textarea>

    </form>'''

@app.route('/file1/<file1>/file2/<file2>') 
def compute_similarity_of_files(file1: str, file2: str) -> str:
    """This function computes first two embeddings for the contents of two files
    and then computes the cosine similarity of the two embeddings. The 
    cosine similarity is returned as string in a web form. 

    Args:
        file1 (str): This parameter is the name of the first file for which the 
            cosine similarity of its content with the content of the second 
            file is computed. The file should be in the same directory as this
            program.
        file2 (str): This parameter is the name of the second file for which 
            the cosine similarity of its content with the content of the first
            file is computed. The file should be in the same directory as this
            program.

    Returns: 
        str: A string is returned that contains html code for a web from that
            contains two labels file1 and file2 and the names of the files the 
            user specified. In a textfield the cosine similarity of the content 
            of the two files is displayed. If the embedding for one of the 
            files cannot be computed, there is a message that the file is 
            probably too large in the textfield.     
    """
    # Test if files exist.
    if not ((path.exists(file1) and path.exists(file2))):
      return "<p>At least one file does not exist on the server.</p>"

    files = [file1, file2]
    embeddings = []
    # Compute embeddings for content of the files.
    for file in files:
        fileinput = open(file, 'r')
        embeddings.append(embedding_from_string(fileinput.read(), 
                                                "text-embedding-ada-002"))
        fileinput.close()
        
    text = ""
    # Test if embeddings could be computed.
    for i in range(0,2):
        if (embeddings[i] == [None]):
            text += files[i] + " is too large to compute an embedding for it. "
    if not text:  # Test if both embeddings could be computed.
        # Compute cosine similarity of both embeddings and display it.
        similarity = cosine_similarity(embeddings[0], embeddings[1])
        text += "The cosine similarity between " + file1 + " and " + file2 + " \
            is " + str(similarity) + "."
    return '''
          <label id="file1">file1: '''+file1+'''</label> <br>
          <label id="file2">file2: '''+file2+'''</label> <br>
  
          <form>
          <textarea id="file1content" name="file1" rows="10" cols="30">'''\
              +text+'''</textarea>

          </form>'''

if __name__ == '__main__':
    app.run()
