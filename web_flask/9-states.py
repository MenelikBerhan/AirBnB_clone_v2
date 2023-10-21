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


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays a list of states or list of cities for a state"""
    if id is None:
        states = storage.all(State).values()
        return render_template('9-states.html', states=states, id=None)
    else:
        states = storage.all(State)
        if ('State.' + escape(id)) in states:
            state = states['State.' + escape(id)]
            return render_template('9-states.html', state=state)
        else:
            return render_template('9-states.html', state=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
