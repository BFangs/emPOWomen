from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
from datetime import datetime
from model import (User, Scholarship, Category, UserCategory, ScholarshipCategory, UserCategory)
from model import db


class Scraper(object):

    def __init__(self, website):
        self.website = website
        self.results = []
        self.time = datetime.now()

    def start_scrape(self):
        html = urlopen(self.website).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_from_table(self):
        """for scholarships.com specific table configuration returns scholarship info"""
        soup = self.start_scrape()
        rows = soup.find_all("tr")
        for row in rows[1:]:
            print row
            link = row.find("a")["href"]
            try:
                link = self.get_real_link(link)
            except:
                link = "https://www.scholarships.com" + link
            try:
                amount = row.find("td", "scholamt").text.strip()
                no_comma = amount.replace(',', '')
                amount_num = int(no_comma.replace('$', ''))
            except:
                amount_num = None
            name = row.find("td", "scholtitle").text
            try:
                date = row.find("td", "scholdd").text
                deadline = datetime.strptime(date, "%m/%d/%Y")
            except:
                deadline = None
            scholarship = {"url": link,
                           "scholarship_name": name,
                           "amount": amount_num,
                           "deadline": deadline}
            print scholarship
            self.results.append(scholarship)
        return self.results

    @staticmethod
    def get_real_link(url):
        """get actual links from scholarships.com table"""
        base = "https://www.scholarships.com"
        html = urlopen(base+url).read()
        soup = BeautifulSoup(html, "html.parser")
        button = soup(text='Apply Now!')
        tag = button[0].parent["href"]
        link = tag.split()[0][26:-2]
        return link


    @classmethod
    def load_all(cls, website):
        data = cls(website)
        data.get_from_table()
        for entry in data.results:
            entered = Scholarship(**entry)
            db.session.add(entered)
        db.session.commit()
