#!/usr/bin/python3
"""a script that starts a flask application"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """display hello hbnb"""
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb_page():
    """display hbnb"""
    return 'HBNB'


@app.route("/c/<text>", strict_slashes=False)
def C_is_fun_page(text):
    """display c plus a variable"""
    newText = text.replace('_', ' ')
    return f'C {newText}'


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_page(text="is_cool"):
    """display c plus a variable"""
    newText = text.replace('_', ' ')
    return f'Python {newText}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
