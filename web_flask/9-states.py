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
    """Displays a list of states"""
    if id is None:
        states = sorted(storage.all(State).values(),
                        key=lambda state: state.name)
        return render_template('9-states.html', states=states, id=None)
    else:
        states = storage.all(State)
        if ('State.' + escape(id)) in states:
            state = states['State.' + escape(id)]
            cities = state.cities
            return render_template('9-states.html', state_name=state.name,
                                   cities=cities)
        else:
            return render_template('9-states.html', state_name=None,
                                   cities=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
