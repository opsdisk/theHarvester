#!/usr/bin/env python
import argparse
import google  # https://pypi.python.org/pypi/google
import re
import socket
import sys
import time
import urllib2


class TheHarvester:

    def __init__(self, dataSource, domain, searchMax, saveEmails, delay, urlTimeout):
        self.dataSource = dataSource
        self.domain = domain
        
        self.searchMax = searchMax
        if self.searchMax < 100:
            self.numMax = self.searchMax
        else:
            self.numMax = 100
            
        self.saveEmails = saveEmails
        self.delay = delay
        self.urlTimeout = urlTimeout
        self.allEmails = []
        
        socket.setdefaulttimeout(self.urlTimeout)

    def go(self):
        
        if self.dataSource == "all":
            self.google_search()  
            self.pgp_search()
        elif self.dataSource == "google":
            self.google_search()
        elif self.dataSource == "pgp":
            self.pgp_search()
        else:
            print "[-] Unknown data source type"
            sys.exit()

        # Display emails
        self.display_emails()

        # Save emails to file
        if self.saveEmails and self.allEmails:
            fh = open(self.domain + '_' + get_timestamp() + '.txt', 'a')
            for email in self.parsedEmails:
                fh.write(email + "\n")
            fh.close() 

    def google_search(self):
        # Retrieve pages based on domain search query
        print "[*] Searching for email addresses in " + str(self.searchMax) + " pages and waiting " + str(self.delay) + " seconds between searches"
        
        # Search for emails not within the domain's site (-site:<domain>)
        query = self.domain + " -site:" + self.domain
        print "[*] Searching for emails not within the domain's site: " + query
        for url in google.search(query, start=0, stop=self.searchMax, num=self.numMax, pause=self.delay):
            self.find_emails(url)  
            
        # Search for emails within the domain's site (site:<domain>)
        query = "site:" + self.domain
        print "[*] Searching for emails within the domain's site: " + query
        for url in google.search(query, start=0, stop=self.searchMax, num=self.numMax, pause=self.delay):
            self.find_emails(url)         

    def pgp_search(self):
        url = "https://pgp.mit.edu/pks/lookup?search=" + self.domain + "&op=index"       
        self.find_emails(url)
        
    def find_emails(self, url):
        try:
            print "[+] Scraping any emails from: " + url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-zA-Z0-9.-]*" + self.domain, response.read(), re.I)
            if emails:
                for e in emails:
                    self.allEmails.append(e)
        except:
            print "[-] Timed out after " + str(self.urlTimeout) + " seconds...can't reach url: " + url
    
    def display_emails(self):
        if not self.allEmails:
            print "[-] No emails found"
        else:
            self.parsedEmails = list(sorted(set([element.lower() for element in self.allEmails])))
            print "\n[+] " + str(len(self.parsedEmails)) + " unique emails found:"
            print "---------------------------"
            for email in self.parsedEmails:
                print email


def get_timestamp():
    now = time.localtime()
    timestamp = time.strftime('%Y%m%d_%H%M%S', now)
    return timestamp
 
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='theHarvester2')
    dataSources = ['all', 'google', 'pgp']
    parser.add_argument('-b', dest='dataSource', action='store', required=True, help='Specify data source (' + ', '.join(dataSources) + ')')
    parser.add_argument('-d', dest='domain', action='store', required=True, help='Domain to search')
    parser.add_argument('-l', dest='searchMax', action='store', type=int, default=100, help='Maximum results to search (default and minimum is 100)')
    parser.add_argument('-f', dest='saveEmails', action='store_true', default=False, help='Save the emails to emails_<TIMESTAMP>.txt file')
    parser.add_argument('-e', dest='delay', action='store', type=float, default=7.0, help='Delay (in seconds) between searches.  If it\'s too small Google may block your IP, too big and your search may take a while.')
    parser.add_argument('-t', dest='urlTimeout', action='store', type=int, default=5, help='Number of seconds to wait before timeout for unreachable/stale pages (default 5)')

    args = parser.parse_args()

    if args.dataSource not in dataSources: #"bing", "bing_api", "exalead", "google", "google_profiles", "jigsaw", "linkedin", "people123", "pgp", "yandex"):
        print "[-] Invalid search engine...specify (" + ', '.join(dataSources) + ")"
        sys.exit()
    if not args.domain:
        print "[!] Specify a domain (-d)"
        sys.exit()
    if args.delay < 0:
        print "[!] Delay (-e) must be greater than 0"
        sys.exit()
    if args.urlTimeout < 0:
        print "[!] URL timeout (-t) must be greater than 0"
        sys.exit()

    #print vars(args)
    th = TheHarvester(**vars(args))
    th.go()

    print "\n[+] Done!"
