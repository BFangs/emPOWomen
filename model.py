from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

# connecting to the PostgreSQL database through flask_sqlalchemy helper library
db = SQLAlchemy()

pacific = pytz.timezone('US/Pacific')

def connect_to_db(app, db_url='postgresql:///scholarships'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)

    def __repr__ (self):
        """Displayed when called"""

        return "<%s>"%(self.user_name)


class Scholarship(db.Model):
    """Scholarship table"""

    __tablename__ = "scholarships"

    scholarship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scholarship_name = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    annual = db.Column(db.Boolean)
    deadline = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=pacific))
    url = db.Column(db.String(100), unique=True)

    def __repr__(self):
        """Displayed when called"""

        return"<%s>"%(self.scholarship_name)


class Category(db.Model):
    """Category table"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key= True)
    category_name = db.Column(db.String(25))

    def __repr__(self):
        """Displayed when called"""

        return"<%s>"%(self.category_name)


class UserCategory(db.Model):
    """User's preferred categories table"""

    __tablename__ = "user_categories"


    uc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    users = db.relationship('User', backref='user_categories')
    categories = db.relationship('Category', backref='user_categories')

    def __repr__(self):
        """Displayed when called"""

        return"<%s>"%(self.uc_id)


class ScholarshipCategory(db.Model):
    """User's preferred categories table"""

    __tablename__ = "scholarship_categories"


    sc_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.scholarship_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    scholarships = db.relationship('Scholarship', backref='scholarship_categories')
    categories = db.relationship('Category', backref='scholarship_categries')

    def __repr__(self):
        """Displayed when called"""

        return"<%s>"%(self.sc_id)


class UserScholarship(db.Model):
    """"User's preferred scholarships table"""

    __tablename__ = "user_scholarships"

    us_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.scholarship_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    users = db.relationship('User', backref='user_scholarships')
    scholarships = db.relationship('Scholarship', backref='user_scholarships')

    def __repr__(self):
        """Displayed when called"""

        return"<%s>"%(self.us_id)


class URL(db.Model):
    """URLS to scrape"""

    __tablename__="urls"

    url_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Displayed when called"""

        return"<%s>"(self.url_id)


if __name__ == "__main__":
    # when running module interactively will allow working with database directly
    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
