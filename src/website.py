from os import path

from flask import Flask
from openai.embeddings_utils import cosine_similarity

from compute_embedding import embedding_from_string

app = Flask(__name__)

@app.route('/')
def home():
    return '''<form>
  <label for="fname">Enter first file file: </label><br>
  <input type="text" id="file1"><br>
  <label for="lname">Enter second file:</label><br>
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

      }
      else {
        window.open(actualUrl+"/file1/"+f1+"/file2/"+f2);
        }
    }
  </script>

  <form>
  <textarea name="file1" rows="10" cols="30">
  </textarea>

</form>'''

@app.route('/file1/<file1>/file2/<file2>')
def compute_similarity_of_files(file1: str, file2: str):
    """This function computes first two embeddings for the contents of two files
           and then computes the cosine similarity of the two embeddings. The 
           cosine similarity is returned as string in a web form. 

      Args:
          file1 (str): This parameter is the name of the first file for which 
              the cosine similarity of its content with the content of the 
              second file is computed.
          file2 (str): This parameter is the name of the second file for which 
              the cosine similarity of its content with the content of the first
              file is computed.

      Returns: 
          
    """
    # Test if files exist.
    if not ((path.exists(file1) and path.exists(file2))):
      return "<p>File does not exist</p>"

    # Get content of files in one string each.
    file1input = open(file1, "r")
    file2input = open(file2, "r")
    file1text=file1input.read()
    file2text=file2input.read()
    file1input.close()
    file2input.close()
    
    # Compute embeddings for both files.
    file1_embedding = embedding_from_string(file1text, "text-embedding-ada-002")
    file2_embedding = embedding_from_string(file2text, "text-embedding-ada-002")
    text = ""
    # Test if embeddings could be computed.
    if (file1_embedding is None):
        text += "File 1 " + file1 + " is too large to compute an embedding for \
            it."
    elif (file2_embedding is None):
        text += "File 2 " + file2 + " is too large to compute an embedding for \
            it."
    else:
        # Compute cosine similarity of both embeddings and dispaly it.
        similarity = cosine_similarity(file1_embedding, file2_embedding)
        text += "The cosine similarity between " + file1 + " and " + file2 + " \
            is " + str(similarity) + "."
    return '''
          <label id="file1">file1: '''+file1+'''</label> <br>
          <label id="file2">file2: '''+file2+'''</label> <br>
  
          <form>
          <textarea id="file1content" name="file1" rows="10" cols="30">'''+text+'''</textarea>

          </form>'''

if __name__ == '__main__':
    app.run()