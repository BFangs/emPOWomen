import schedule
import time
from datetime import datetime, timedelta
from model import (User, Scholarship, UserScholarship, connect_to_db, db)
from server import app
import os
import sendgrid
from sendgrid.helpers.mail import *
apikey=os.environ.get('SENDGRID_API_KEY')
connect_to_db(app)

def reminder_job():
    now = datetime.now()
    end = now + timedelta(weeks=2)
    to_send = queue_upcoming(now, end)
    for item in to_send:
        name, deadline, url, amount, saved_thing = item
        email = saved_thing.users.user_email
        try:
            sg = sendgrid.SendGridAPIClient(apikey)
            from_email = Email("noreply@empowomen.com")
            to_email = Email(email)
            subject = "Scholarship Notification"
            content = Content("text/plain", "We would like to send you a reminder to apply for" + name +
                              "! You could get " + amount + "to help further your education.\n\
                              Hurry and make sure you don't miss the deadline at:\n" +
                              deadline + ".\nGo to this link to apply now! " + url)
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print "Sending email"
            saved_thing.sent = True
        except:
            print "failed to send message to user " + email
    db.session.commit()

def digest_job():
    now = datetime.now()
    last = now - timedelta(weeks=1)
    to_send = queue_new_entries(now, last)
    compiled
    # not finished with cron job!


def queue_new_entries(now, last):
    new = Scholarship.query.filter(Scholarship.created<=now, Scholarship.created>=last).all()
    to_send = []
    for item in new:
        info = {"name": item.scholarship_name}
        if item.deadline:
            info["deadline": item.deadline]
        if item.amount:
            info["amount": item.amount]
        if item.url:
            info["url": item.url]
        if item.organization:
            info["organization": item.organization]
        to_send.append(info)
    return to_send


def queue_upcoming(now, end):
    saved = UserScholarship.query.filter(UserScholarship.sent==False).all()
    to_send = []
    for one in saved:
        scholarship = one.scholarships
        if now < scholarship.deadline and scholarship.deadline < end:
            to_send.append((scholarship.scholarship_name,
                            scholarship.deadline,
                            scholarship.url,
                            scholarship.amount,
                            one))
    return to_send



schedule.every().day.at("10:30").do(reminder_job)
#schedule.every().monday.at("10:00").do(digest_job)

while 1:
    schedule.run_pending()
    time.sleep(1)
