from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''<form>
  <label for="fname">Enter first file file: </label><br>
  <input type="text" id="file1"><br>
  <label for="lname">Enter second file:</label><br>
  <input type="text" id="file2"><br><br>

  <button onclick="myFunction()"> Read in files </button> <br><br>

  <p id="demo"> </p>

  <script>
    function myFunction() {
      let f1 = document.getElementById("file1").value;
      let f2 = document.getElementById("file2").value;
      window.open("https://apphub-s-luresz.wolke.uni-greifswald.de/proxy/5000/file1/"+f1+"/file2/"+f2);
    }
  </script>

  <form>
  <textarea name="file1" rows="10" cols="30">
  </textarea>

  <form>
  <textarea name="file2" rows="10" cols="30">
  </textarea>

</form>'''

@app.route('/file1/<file1>/file2/<file2>')
def input_files(file1, file2):
  file1input = open(file1, "r")
  file2input = open(file2, "r")

  file1text=file1input.read()
  file2text=file2input.read()
  
  #print(file1text.read())

  return '''
  <label id="file1">file1: '''+file1+'''</label> <br>
  <label id="file2">file2: '''+file2+'''</label> <br>
  
  <form>
  <textarea id="file1content" name="file1" rows="10" cols="30">'''+file1text+'''</textarea>

  <textarea id ="file2content" name="file2" rows="10" cols="30">'''+file2text+'''</textarea>

</form>
'''

if __name__ == '__main__':
    app.run()