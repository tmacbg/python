#!/usr/bin/python


import mechanize
import cookielib
import time
import sys

br = mechanize.Browser()

#cj = cookielib.LWPCookieJar()
#br.set_cookiejar(cj)

br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Ubuntu/3.0.1-1.fc9 Firefox/3.0.1')]
start_timer = time.time()
r = br.open('http://affordable-hotels.co.uk/')
r.read()
html = r.read()
latency = time.time() - start_timer
print latency

#html = r.read()

print html


#print r.info()
