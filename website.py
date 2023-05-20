from flask import Flask

file1text = open("test1.txt", "r")
file2text = open("test2.txt", "r")

testtext = "Das ist ein Testtext"

t1=file1text.read()

print(file1text.read())
print(file2text.read())


app = Flask(__name__)

@app.route('/')
def home():
    return '''<form>
  <label for="fname">Enter first file file: </label><br>
  <input type="text" id="fname" name="fname"><br>
  <label for="lname">Enter second file:</label><br>
  <input type="text" id="lname" name="lname"><br><br>

  <input type="submit"> <br><br>

  <form>
  <textarea name="file1" rows="10" cols="30">''' +t1+'''
  </textarea>

  <form>
  <textarea name="file2" rows="10" cols="30">'''+testtext+'''
  </textarea>

</form>'''

if __name__ == '__main__':
    app.run()