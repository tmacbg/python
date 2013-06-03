#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup
#from bs4 import SoupStrainer
import urllib
a = 20
b = 30
f = { 'd' : '11' }
f2 = urllib.urlencode(f)
url = 'http://www.toptable.co.uk/nextavailabletable.aspx?hpu=1455029583&shpu=1&rid=81850&m=3083&d=12%2f06%2f2013+20%3a00%3a00&p=2&msg=Unfortunately+there+are+no+tables+available+for+this+date.+The+Fat+Duck+releases+availability+2+months+in+advance+at+10AM%2c+please+try+your+search+again+then.%0D%0A+%0D%0AAlternatively%2c+you+can+add+your+name+to+the+Waitlist%3a+++title%3d+Click+here+for+the+Fat+Duck+Waiting+List++++http%3a%2f%2ffatduck.d3r.com%2fwaiting-list+++Click+here+for+the+Fat+Duck+Waiting+List++%0D%0A++Please+note+we+are+closed+every+Sunday+and+Monday.+'

#print url
urldata = urllib2.urlopen(url, timeout = 25).read()

soup = BeautifulSoup(urldata, "html5lib")

#print soup

print soup('table')[2].findAll('tr')[1].findAll('td')[1].prettify()


#print soup('table')[2].findAll('tr')[1].findAll('td')[1].findAll('td')
