#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
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


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays 'n is a number' if n is an integer"""
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_even(n):
    """Display a HTML page only if n is an integer"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
