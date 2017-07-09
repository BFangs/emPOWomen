from sqlalchemy import func
from model import (User, Scholarship, Category, UserCategory, ScholarshipCategory, UserCategory)
from flask import Flask
from model import connect_to_db, db
from datetime import datetime
from scrape import Scraper


def create_categories():
    """Creates categories in categories tables"""

    print "Categories"

    Category.query.delete()

    woman_of_color = Category(category_name="Women of Color")
    LGBTQ = Category(category_name="LGBTQ")
    moms = Category(category_name="Mothers")
    low_income = Category(category_name="Low Income")
    native_american= Category(category_name="Native American")
    visas = Category(category_name="Visa")
    first_gen = Category(category_name="First Generation")
    graduate_students = Category(category_name="Graduate Students")
    asian = Category(category_name="Asian")

    db.session.add_all([woman_of_color, LGBTQ, moms, low_income,
                        native_american, visas, first_gen,
                        graduate_students, asian])
    db.session.commit()


def create_scholarships():
    """creates types in the types table"""

    print "Scholarships"

    Scholarship.query.delete()

    one = Scholarship(scholarship_name = 'TheAWG Minority Scholarship',
                      organization='The Association for Women Geoscientists (AWG) Foundation',
                      amount=6000,
                      deadline= datetime.datetime(2018, 6, 30, 0, 0),
                      annual = True
                      url='http://usascholarships.com/awg-minority-scholarship/')
    two = Scholarship(scholarship_name = 'The AICPA Fellowship for Minority Doctoral Students',
                      organization='American Institute of CPAs',
                      amount=12000,
                      deadline=datetime.datetime(2017, 5, 15, 0, 0),
                      url='http://www.aicpa.org/Career/DiversityInitiatives/Pages/fmds.aspx')
    three = Scholarship(scholarship_name = 'The Asian Women In Business Scholarship',
                      organization='The AWIB Scholarship Fund',
                      amount=2500,
                      url='http://www.awib.org/index.cfm?fuseaction=Page.ViewPage&PageID=811')

    db.session.add_all([one, two, three])
    db.session.commit()

def create_scholarships_website():
    """creates scholarships in scholarships table"""
    Scraper.load_all("https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/gender/female")


def create_scholarship_categories():

    print "Scholarship Categories"

    one = ScholarshipCategory(scholarship_id=1, category_id=1)

    two = ScholarshipCategory(scholarship_id=2, category_id=1)

    three = ScholarshipCategory(scholarship_id=2, category_id=8)

    four = ScholarshipCategory(scholarship_id=3, category_id=8)

    five = ScholarshipCategory(scholarship_id=3, category_id=9)

    db.session.add_all([one, two, three, four, five])
    db.session.commit()

if __name__ == "__main__":
    #later can import app from server
    app = Flask(__name__)
    connect_to_db(app)
    db.create_all()


    create_scholarships()
    create_categories()
    create_scholarship_categories()
