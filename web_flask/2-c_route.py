#!/usr/bin/python3
"""Starts Flask web application

Application listens on 0.0.0.0, port 5000
Routes:
    /: Display 'Hello HBNB!'
    /hbnb: Displays 'HBNB'
    /c/<text>: Display 'C' followed by the value of <text>
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Display 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Display 'C' followed by value of <text>"""
    text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
