import schedule
import time
from datetime import datetime, timedelta
from model import (User, Scholarship, UserScholarship, connect_to_db, db)
from server import app
import os
from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import *

connect_to_db(app)

def job():


schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
