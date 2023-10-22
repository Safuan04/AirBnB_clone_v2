#!/usr/bin/python3
"""Impoerting necessary modules"""

from flask import Flask, render_template
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


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def py_text(text="is cool"):
    """This is a rout that displays:
        “Python ” followed by the value of the text variable """
    return f"Python {escape(text).replace('_', ' ')}"


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """This is a rout that displays: “n is a number” only if n is an integer"""
    return f"{escape(n)} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_1(n):
    """This is a rout that displays a HTML page only if n is an integer
        H1 tag: “Number: n” inside the tag BODY"""
    return render_template('5-number.html', number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_2(n):
    """This is a rout that displays a HTML page only if n is an integer
        H1 tag: “Number: n is even|odd” inside the tag BODY"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    """Run the application on 0.0.0.0 and port 5000"""
    app.run(host='0.0.0.0', port=5000, debug=True)
