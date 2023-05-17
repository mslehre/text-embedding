from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''<form>
  <label for="fname">Enter first file file: </label><br>
  <input type="text" id="fname" name="fname"><br>
  <label for="lname">Enter second file:</label><br>
  <input type="text" id="lname" name="lname"><br><br>

  <input type="submit">
</form>'''

if __name__ == '__main__':
    app.run()