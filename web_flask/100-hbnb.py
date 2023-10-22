#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User

app = Flask(__name__)


@app.teardown_appcontext
def remove_session(exception):
    """Removes the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """Display a HTML page like 8-index.html"""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    users = storage.all(User)
    return render_template('100-hbnb.html', states=states, amenities=amenities,
                           places=places, users=users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
