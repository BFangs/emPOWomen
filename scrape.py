from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
from datetime import datetime


def start_scrape(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_from_table(url="https://www.scholarships.com/financial-aid/college-scholarships/scholarship-directory/gender/female"):
    """for specific website table configuration returns scholarship info"""
    soup = start_scrape(url)
    rows = soup.find_all("tr")
    all_entries = []
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
        all_entries.append(scholarship)
    return all_entries
