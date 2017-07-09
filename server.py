from jinja2 import StrictUndefined
from flask import (Flask, session, render_template, request, jsonify)
import hashlib
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db
from gevent.wsgi import WSGIServer

app = Flask(__name__)
app.secret_key = "GOFEMINISM"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    """Homepage."""

    return render_template("home.html")


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    DebugToolbarExtension(app)
