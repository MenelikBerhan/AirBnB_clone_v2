#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask
from markupsafe import escape
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def root():
    """Returns text for root index"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns text for /hbnb path"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def cText(text):
    """Returns 'C text' for /c/<text> path"""
    return f"C {escape(text).replace('_', ' ')}"


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythonText(text='is cool'):
    """Returns 'Python text' for /c/<text> path"""
    return f"Python {escape(text).replace('_', ' ')}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
