from flask import Flask
from os import path

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


  <button onclick="myFunction()"> Read in file texts </button> <br><br>

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
        alert("The file text can not be empty!");
      }
      else {
        document.getElementById("file1a2").value=f1+f2;
        }
    }
  </script>

  <form>
  <textarea id="file1a2" rows="10" cols="30">
  </textarea>

</form>'''

if __name__ == '__main__':
    app.run()