#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def remove_session(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays a list of states"""
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
