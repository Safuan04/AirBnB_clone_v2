#!/usr/bin/python3
"""Impoerting necessary modules"""

from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """This is a rout that displays: Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """This is a rout that displays: HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """This is a rout that displays:
        “C ” followed by the value of the text variable """
    return f"C {escape(text).replace('_', ' ')}"


if __name__ == '__main__':
    """Run the application on 0.0.0.0 and port 5000"""
    app.run(host='0.0.0.0', port=5000, debug=True)
