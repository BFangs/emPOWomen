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


@app.route('/login' methods=["POST"])
def login():
    """loging in"""

    email = request.form.get('email').lower()
    password = request.form.get('password')
    user = User.query.filter(User.email==email).first()
    if user:
        password = password.encode('utf8') 
        hashedpass = q.password.encode('utf8') 
        if bcrypt.checkpw(password, hashedpass):
            session['user_id'] = user.user_id
            return redirect('/')
    else:
        flash("Username or password not found")
        return redirect ('/login')


@app.route('/logout' methods=['POST'])
def logout():
    """loging out"""

    del session['user_id']

    return redirect('/')


@app.route('/save' methods = ['POST'])
def save_scholarship():
    """save scholarship to user's profile"""

    if 'user_id' in session:
        

    else:
        flash("Login to save")
        return redirect('/login')


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
    DebugToolbarExtension(app)
