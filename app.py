import os
from flask import Flask, session

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route("/")
def root():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run()
