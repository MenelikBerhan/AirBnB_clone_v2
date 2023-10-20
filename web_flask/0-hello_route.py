#!/usr/bin/python3
"""starts a Flask web application"""
from web_flask import app


@app.route('/', strict_slashes=False)
def root():
    """Returns text for root index"""
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
