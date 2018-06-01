from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

# Alternative to `flask run` command, but not recommended for development
# See here: http://flask.pocoo.org/docs/1.0/server/#server
if __name__ == "__main__":
    app.run()
