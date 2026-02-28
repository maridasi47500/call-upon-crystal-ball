from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>live your daily life </p><p>unlock the meaning of a place : choose <select><option>gem linked to a place </option><option>technology/programming language</option><option>a symbolic instrument</option><option>call upon AI </option></select></p>"
