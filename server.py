from jinja2 import StrictUndefined
from flask import (Flask, session, render_template, request, jsonify, redirect, flash)
import hashlib
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, User, Scholarship, Category, UserCategory, UserScholarship, ScholarshipCategory, db #add db
# from gevent.wsgi import WSGIServer
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "GOFEMINISM"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def display_homepage():
    """displays homepage"""

    scholarships= Scholarship.query.all()
    scholarships_list = []
    for scholarship in scholarships:
        scholarship_id = scholarship.scholarship_id
        scholarship_categories = ScholarshipCategory.query.filter(ScholarshipCategory.scholarship_id==scholarship_id).all()
        category_list =[]
        for sc in scholarship_categories:
            category_list.append(sc.categories.category_name)
        scholarships_list.append((scholarship, category_list))

    return render_template('home.html', scholarships=scholarships_list)


@app.route('/login', methods=["POST"])
def login():
    """logs in user"""

    email = request.form.get('user_email').lower()
    password = request.form.get('password')
    user = User.query.filter(User.user_email==email).first()
    if user:
        password = password.encode('utf8')
        hashedpass = user.password.encode('utf8')
        if bcrypt.checkpw(password, hashedpass):
            session['user_id'] = user.user_id
            return redirect('/get_user_scholar')
        else:
            flash('Incorrect password')
            return redirect('/')
    else:
        flash("Email not found")
        return redirect('/login')


@app.route('/logout')
def logout():
    """logs out user"""

    del session['user_id']

    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    """registers a new user"""

    email = request.form.get('user_email') # changed
    user = User.query.filter(User.user_email==email).first()

    if user:
        flash("An account already exists for this email. Please log in.")
        return redirect('/')

    password = request.form.get('password').rstrip()
    password = password.encode('utf8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    name = request.form.get('user_name') # changed

    new_user = User(user_email=email, password=hashed, user_name=name) #user_name #user_email
    db.session.add(new_user) #
    db.session.commit() #

    session['user_id'] = new_user.user_id

    return redirect('/get_user_scholar')


@app.route('/save', methods = ['POST'])
def save_scholarship():
    """save scholarship to user's profile"""

    scholarship_id = request.form.get("scholarship_id")

    if 'user_id' in session:
        user_id = session['user_id']
        user_scholarship = UserScholarship(scholarship_id=scholarship_id, user_id=user_id)
        db.session.add(user_scholarship)
        db.session.commit()
        return redirect('/get_user_scholar')
    else:
        flash("Login to save")
        return redirect('/login')


@app.route('/user/<user_id>')
def show_users(user_id):
    """shows user profile"""

    current_user = User.query.filter(User.user_id==user_id).first()

    categories = []

    user_categories = UserCategory.query.filter(UserCategory.user_id==user_id).all()

    for user_category in user_categories:
        category = Category.query.filter(Category.category_id==user_category.category_id).first()
        categories.append(category.category_name)

    all_categories = Category.query.all()

    all_categories_list = []

    for category in all_categories:
        all_categories_list.append(category.category_name)

    non_user_categories = set(all_categories_list) - set(categories)

    return render_template('profile.html', user=current_user, user_categories=categories, non_user_categories=non_user_categories)


@app.route('/scholarships/<user_id>')
def show_scholarships(user_id):
    """shows all scholarships?"""

    scholarships =[]
    user_id = int(session['user_id'])
    user_scholarships = UserScholarship.query.filter(UserScholarship.user_id==user_id).all()
    for user_scholarship in user_scholarships:
        scholarship_id = user_scholarship.scholarship_id
        scholarship = Scholarship.query.get(scholarship_id)
        scholarships.append(scholarship)

    return render_template('saved.html', scholarships=scholarships)


@app.route('/add_category', methods=["POST"])
def add_user_category():
    """adds a category to user profile"""

    categories = request.form.getlist('categories')

    user_id = int(session['user_id'])

    for category in categories:
        category = Category.query.filter(Category.category_name == category).first()
        user_category = UserCategory(user_id= user_id, category_id = category.category_id)
        db.session.add(user_category)
        db.session.commit()
    return redirect('/user/%s'%(str(user_id)))


@app.route('/get_user_scholar')
def get_users_scholarship():
    """displays scholarships that fit user's categories"""

    scholarships =[]
    user_id = int(session['user_id'])
    user = User.query.filter(User.user_id==user_id).first()

    user_categories = UserCategory.query.filter(UserCategory.user_id==int(session['user_id'])).all()
    for user_category in user_categories:
        category_id=user_category.category_id
        scholarship_categories = ScholarshipCategory.query.filter(ScholarshipCategory.category_id==category_id).all()
        for scholarship_category in scholarship_categories:
            scholarships.append(Scholarship.query.filter(Scholarship.scholarship_id==scholarship_category.scholarship_id))

    scholarships_query= Scholarship.query.all()
    scholarships_list = []
    for scholarship in scholarships_query:
        scholarship_id = scholarship.scholarship_id
        scholarship_categories = ScholarshipCategory.query.filter(ScholarshipCategory.scholarship_id==scholarship_id).all()
        category_list =[]
        for sc in scholarship_categories:
            category_list.append(sc.categories.category_name)
        scholarships_list.append((scholarship, category_list))

    return render_template('results.html', user=user, scholarships=scholarships, scholarships_list=scholarships_list)



if __name__ == "__main__":

    # app.debug = True
    # app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.run(port=int(os.environ['PORT']), host='0.0.0.0')
    # DebugToolbarExtension(app)
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
