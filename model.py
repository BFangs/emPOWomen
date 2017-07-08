from flask_sqlalchemy import SQLAlchemy
# connecting to the PostgreSQL database through flask_sqlalchemy helper library
db = SQLAlchemy()


def connect_to_db(app, db_url='postgresql:///scholarships'):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # when running module interactively will allow working with database directly
    from server import app
    connect_to_db(app)
    print "Connected to DB."
