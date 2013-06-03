import urllib2
import sys

def internet_on():
    try:
     response = urllib2.urlopen('http://google.com', timeout = 3)
     print True
    except urllib2.URLError as err: 
          pass
          print False
internet_on()
