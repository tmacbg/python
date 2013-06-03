#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib, urllib2

def google_scrape(query):
    address = "http://www.google.com/search?q=%s&num=100&hl=en&start=0" % (urllib.quote_plus(query))
    request = urllib2.Request(address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urllib2.urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page)

    linkdictionary = {}

    for li in soup.findAll('li', attrs={'class':'g'}):
        sLink = li.find('a')
        print sLink['href']
        sSpan = li.find('span', attrs={'class':'st'})
        print sSpan

    return linkdictionary

if __name__ == '__main__':
    links = google_scrape('beautifulsoup')
