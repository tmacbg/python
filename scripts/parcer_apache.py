#!/usr/bin/env python

import time, re
from smtplib import SMTP
import datetime


def sendMail2(ip, url2):

        date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
        toaddr = "nnedelchev@1stonlinesolutions.co.uk"
        cc = ['ba4uty@gmail.com' ]
#        toaddr = "nnedelchev@1stonlinesolutions.co.uk"
#        cc = ['ba4uty@gmail.com']
        fromaddr = 'PPC checker <ppc@cleaningincroydon.co.uk>'
        message_subject = "PPC site enter -  date : " + date
        message_text = "Hello\n\nSince "+date+" IP :\n"+ip+"\n\nLovely regards,\nThe Bot\nP.S. GOOGLE URL :\n"+url2
        message = "From: %s\r\n" % fromaddr + "To: %s\r\n" % toaddr + "CC: %s\r\n" % ",".join(cc) + "Subject: %s\r\n" % message_subject + "\r\n"  + message_text
        toaddrs = [toaddr] + cc
        server = SMTP('192.168.50.211')
        server.set_debuglevel(1)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()



def log():
 src = open('cleaningincroydon.co.uk', 'r')
 dest = open('x.csv', 'w')
 for line in src:
    ip = line[:line.index(' ')]
    dest.write(ip)
    dest.write(':-')
    split_line = line.split()
    print {'remote_host': split_line[0],
	        'URL': split_line[6],
	        'bytes_sent': split_line[9]
	        }
    ip = split_line[0]
    url2 = split_line[6]
   # url = re.search('^[/?gclid=]',split_line[6])
    regex = re.compile('/?gclid=')
   # url = re.search(r"gclid=[\w]", split_line[6])
    url = regex.findall(url2)
    url3 = len(url)
    print url3
    if url3==1 :
        print "URL FOUND !!!! ->>>> IP : %s"  % ip
        sendMail2(ip, url2)
    else :
        print "URL NOT FOUND ---- Continue ---- searching"    
    
    b = split_line[6]
    dest.write(b)
    dest.write('\n')   
 src.close()
 dest.close()

log()
#ip_check()

