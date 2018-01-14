from flask import Flask

app = Flask(__main__)
application = app


@app.route('/')
def hello():
    return "Hello world!"
