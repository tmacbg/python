#!/usr/bin/python


import sys
import json
import ConfigParser
import os.path
import urllib
from termcolor import colored
import easygui as eg
import mechanize
import cookielib
import time
import sys

config = os.path.expanduser("~/.pagespeed-config")
parser = ConfigParser.SafeConfigParser()

#def gui():
#    t = "Check Web Page Speed v 1.0"
#    url = eg.enterbox(msg='Enter web site URL.', title='Web Page Speed v 1.0', default =' ', strip = True, image=None, root=None)    
#    return url
#gui()

def gui():
    t = "Check Web Page Speed v 1.0"
    url2 = eg.enterbox(msg='Enter web site URL.', title='Web Page Speed v 1.0', default =' ', strip = True, image=None, root=None)
 #   eg.exceptionbox(msg="You entered %s" % url2,title="Web Page Speed v 1.0" )   
 #   return url2
    msg = "Do you want to continue check %s ?" % url2
    title = "Please Confirm to continue"
    if eg.ccbox(msg, title):
       pass
       return url2
    else:
       sys.exit(0)


def out(text):
    eg.codebox(msg='Speed Results', title='Web Page Speed Results', text='%s' % (text))
    eg.msgbox("%s" %text)
#out()
def main():
 try:
     parser.read(config)
     api_key = parser.get('pagespeed', 'API_KEY')
 except:
     print "Unable to read the config file %s. It should look like this:\n" % config
     print "[pagespeed]"
     print "API_KEY = AIzaSyCHpTlqb_2PKmMFkOqXTl0ldcuuoGvqR2I\n"
     print "See https://developers.google.com/speed/docs/insights/v1/getting_started for details on obtaining a key."
     sys.exit()

 try:
    #url = sys.argv[1]
      url = gui()
 except:
     print "URL to check not specified."
     sys.exit()

 if not "http" in url:
     url = "http://%s" % url

 qs = {}
 qs["prettyprint"] = "false"
 qs["key"] = api_key
 qs["strategy"] = "desktop"
 qs["url"] = url

 url2="%s" % url

 

 br = mechanize.Browser()
 br.set_handle_equiv(True)
 br.set_handle_redirect(True)
 br.set_handle_referer(True)
 br.set_handle_robots(False)

 br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

 br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Ubuntu/3.0.1-1.fc9 Firefox/3.0.1')]
 start_timer = time.time()
 r = br.open(url2)
 r.read()
 html = r.read()
 latency = time.time() - start_timer


 endpoint="https://www.googleapis.com/pagespeedonline/v1/runPagespeed?%s" % urllib.urlencode(qs)

 response = urllib.urlopen(endpoint)


 jso = json.load(response)


 total_score = jso["score"]


 print "\nTotal score: %d" % total_score


 print "\nTotal time without 3-rd party: %s" % colored(latency, "red")
 return jso
def main2(jso):
 for short_name, details in jso["formattedResults"]["ruleResults"].items():
     full_name = details["localizedRuleName"]
     score = details["ruleScore"]
     impact = details["ruleImpact"]
    
#    if score == 100:
#        continue

     print "\n%s (%d)" % (full_name, score)


     if "urlBlocks" in details:
         for index, block in enumerate(details["urlBlocks"]):
             header = block["header"]
             summary = header["format"]
 
             if not "args" in header:
                 print summary                 
             else:
                 for index, arg in enumerate(header["args"]):
                     summary = summary.replace("$%d" % (index + 1), arg["value"])
                 print summary

             if not "urls" in block:
                 continue

             for index, url in enumerate(block["urls"]):
                 message = url["result"]["format"]
                 for index, arg in enumerate(url["result"]["args"]):
                     message = message.replace("$%d" % (index + 1), arg["value"])
                 print "  - %s " % message
 eg.textbox(msg='', title=' ', text='Wep site title : %s\n Web site score : %s' %(full_name, score), codebox=0)
 return
t = main()
main2(t)
t2 = main2(t)
eg.msgbox("Web page Speed test %s" %t2)
