from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
from datetime import datetime


class Scraper:

    def __init__(self, url):
        self.url = url
        self.results = []
        self.time = datetime.now()

    def start_scrape(self):
        html = urlopen(self.url).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def get_from_table(self):
        """for scholarships.com specific table configuration returns scholarship info"""
        soup = start_scrape(self.url)
        rows = soup.find_all("tr")
        for row in rows[1:]:
            print row
            link = row.find("a")["href"]
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
            scholarship = {"link": link,
                           "name": name,
                           "amount": amount_num,
                           "date": deadline}
            print scholarship
            self.results.append(scholarship)
        return self.results

    def 
