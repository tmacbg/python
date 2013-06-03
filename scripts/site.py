#!/usr/bin/python

"""
to install:
# pip install beautifulsoup4  OR apt-get install python-bs4
# apt-get install python-html5lib
# apt-get install python-mysqldb
"""

import urllib2
import sys
import re
import time
import MySQLdb as mdb
from time import sleep
from bs4 import BeautifulSoup
import os
from sst.actions import *
import easygui as eg


def mysqlInsert(domain_name, load_time, t):
	print load_time;
        con = None
	if load_time > 300:
                load_time2 = str(load_time)
		os.system("echo "+ domain_name +" >> /root/lyubo/down_domains")	
	        os.system("echo %s %s %s >> /root/lyubo/down_domains4" % (url, load_time2, t)) 
        try:
                con = mdb.connect('192.168.50.211', 'sitedxr_stats', 'Stats123', 'sitedxr_dom')
                cur = con.cursor()
                data = "INSERT INTO domains_stats ( domain , load_time , check_time  )  VALUES ( '"+ str(domain_name) + "', '%f' ,  NOW() )" % (load_time)
                cur.execute(data)
                con.commit()
        except mdb.Error, e:
                print "mysqlInsert: ",e
                sys.exit(1)
        finally:
                if con:
                        con.close()
#url='http://' + str(sys.argv[1])

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

url2 = gui()
url = 'http://' + str(url2)

def suspended(url):
    urldata = urllib2.urlopen(url, timeout = 25 ).read()
    try:
    #  urldata = urllib2.urlopen(url, timeout = 25 ).read()
      s = BeautifulSoup(urldata, "html5lib")
      t = s.title.string
      print t
      if t == "Account Suspended":
        print "%s --- Suspended" % (url)
      #  return
        exit(1)
      elif t == "503 Service Temporarily Unavailable": 
        print "Domain ---%s--- 503 | %s" % (url, t)
      elif t == "Default Web Site Page":
        print "Domain ---%s--- Default Web Page | %s" % (url, t)
    except:
        #print t
        #return
        exit(1)
    return
#suspended(url)

def s_loader( url, check ):
        
       # suspended(url)
        
        start_time = time.time()
        urldata = urllib2.urlopen(url, timeout = 25 ).read()
        load_time = time.time() - start_time

	#print "url: "+ url +  " load %f " %(load_time)
	        
	if check == 1 and load_time > 5:
		time.sleep(5)
		#print url + " step 1 > 4:  load_time :  %f" %  (load_time)
		load_time2 = s_loader(url, '0')	
	else :
		load_time2 = load_time

        if check == 1 and load_time2 > 5:
                time.sleep(5)
		#print url + " step 2 > 4:  load_time2 : %f" % (load_time2)
                load_time3 = s_loader(url, '0')
	else :
		load_time3 = load_time2

	soup = BeautifulSoup(urldata, "html5lib")
       # print soup
        #print soup.find_all('img')
        #print soup.title.string
        t = soup.title.string
        broi = str(len(soup.find_all('img')))
        if soup.find_all('img') == "[]" and broi==0 or soup.title.string == "Account Suspended":
        #     if soup.title() != "503 Service Temporarily Unavailable":
                print soup.title.string
    #            suspended(urldata) 
		load_time = 999.9
		return load_time
	else:
		return  ( ( load_time + load_time2 + load_time3 ) / 3 )
                print soup.title()
                print "OK it's Working"               
#                suspended()

#url='http://' + str(sys.argv[1])
check = 1

def title(url):
 try:   
    urldata = urllib2.urlopen(url, timeout = 25 ).read()

    soup = BeautifulSoup(urldata, "html5lib")
#    print "OK it's Working"
    print soup.title.string
    return soup.title.string
 except:
    print "Not resolving"
    return
#title()


try:
	load_time = s_loader(url, check)
        t = title(url)
        #eg.msgbox("Web page Speed test %s\n Site Title: %s" %(load_time, t))
        #eg.exceptionbox(msg="You entered %s" % t,title="Web Page Speed v 1.0" )
        eg.textbox(msg='', title=' ', text='Wep site title : %s\n Web site load speed : %s' %(t, load_time), codebox=0)  
except:
        title1 = title(url)
	# check again after 5 sec if it reaaly down
	print "can not check sleep for 8 sec 'n try again"
	sleep(8)
	try: 
		print "try for second time Domain Error : %s" % (title1)
 		load_time = s_loader(url, check)
                #suspended(url)
	except:
		sleep(10)
		try:
			print "try for the next time"
			load_time = s_loader(url, check)
                        title()
		except:
			sleep(6)
			try:
				print "try for the last time"
				load_time = s_loader(url, check)
                                title(url)
			except:
				print " =============== Error loading domain : " + str(url2)
                                title(url)
				notopen = 999.9
                                t = title(url)
                #eg.textbox(msg='', title=' ', text='Wep site title : %s\n Web site load speed : %s' %(t, notopen), codebox=0) 
				mysqlInsert(url2, notopen, t)
                
				# exit(1)
	
# OK add to mysql
#t = title(url)
#print t
t2 = mysqlInsert(url2, load_time, t)
#eg.msgbox("Web page Speed test %s" %t2)
#eg.exceptionbox(msg="You entered %s" % t2,title="Web Page Speed v 1.0" )  