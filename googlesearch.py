import re
import requests
import string
import time

import thparser


class SearchGoogle:

    def __init__(self, domain, limit, delay):
        self.domain = domain
        self.results = ""
        self.totalresults = ""
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.counter = 0
        self.quantity = "100"
        self.limit = limit
        self.delay = delay
  
    def process(self):
        while self.counter <= self.limit:
            self.do_search()
            time.sleep(self.delay)
            self.counter += 100
        self.clean_results()
        emails = re.findall(r"[a-z0-9_.+-]+@[a-z0-9-.]*" + self.domain, self.totalresults, re.I)
        return emails

    def do_search(self):
        url = "https://www.google.com/search?num=" + self.quantity + "&start=" + str(self.counter) + "&hl=en&meta=&q=%40\"" + self.domain + "\"" #%40 = @
        try:
            r = requests.get(url)
        except Exception, e:
            print e
        
        self.results = r.content 
        self.totalresults += self.results

    def clean_results(self):
        self.totalresults = re.sub('<em>', '', self.totalresults) # emphasized text
        self.totalresults = re.sub('<b>', '', self.totalresults) # bold text
        self.totalresults = re.sub('</b>', '', self.totalresults) # bold text
        self.totalresults = re.sub('</em>', '', self.totalresults) # emphasized text
        self.totalresults = re.sub('%2f', ' ', self.totalresults) # / symbol
        self.totalresults = re.sub('%3a', ' ', self.totalresults) # : symbol
        self.totalresults = re.sub('<strong>', '', self.totalresults)
        self.totalresults = re.sub('</strong>', '', self.totalresults)

        for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
            self.totalresults = string.replace(self.totalresults, e, ' ')
