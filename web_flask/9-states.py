#!/usr/bin/python3
"""Starting Flask web app"""
from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def hbnb_states():
    """
    displays a HTML page at /states on 0.0.0.0
    port 5000 and diplays states id and name
    """
    all_states = storage.all(State)
    return render_template('9-states.html', states=all_states, rte=1)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """
    displays a HTML page at /states/<id> on 0.0.0.0
    port 5000 and diplays list of City objects linked to the State
    """
    all_states = storage.all(State)
    for state in all_states.values():
        if (state.id == id):
            return render_template('9-states.html', id=id, states=state, rte=2)
    return render_template('9-states.html', rte=2)


@app.teardown_appcontext
def close_session(exception):
    """closes a sqlalchemy session"""
    storage.close()


if __name__ == "__main__":
    """Run the application on 0.0.0.0 and port 5000"""
    app.run(host='0.0.0.0', port=5000)
