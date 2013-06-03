#!/usr/bin/python

import datetime
from socket import gethostbyname
from termcolor import colored
import MySQLdb as mdb

f = open('failed', 'w')
f.close()
f = open('sitesok', 'w')
f.close()
f = open('siteserror', 'w')
f.close()
f = open('domains.html', 'w')
f.close()
f = open('checkfailed', 'w')
f.close

# Mysql connection
#con = mdb.connect('localhost', 'user', 'test123', 'domains');
# END Mysql connection

with open('/root/sitedxr.com/victorconnect.csv') as input:
 for line in input:
  host, index = line.strip().split(',')
  now = datetime.datetime.now()
  try:
   output = gethostbyname(host)
   if output == index:
    print colored(host,'red'),colored(output,'green')
    now1 = now.strftime("%Y-%m-%d %H:%M")
    f = open('sitesok','a')
    f.write(host + " ==>> " + output + "  " + "SERVER IP : " + " " + index + " " + now1)
#   f.write(host + " , " + output)
    f.write('\n')
    h = open ('domains.html','a') # For monitoring System
    h.write("<a href=http://" + host +"  target=_blank\>" + host + "</a></br>") # Links for monitoring system

# XML File
#    h.write("<link><title>" + host + " -> Netwise2</title><url>http://" + host + "</url></link>")
# End XML FILE

    h.write('\n')

# Mysql database insert domains
#    cur = con.cursor()
#    cur.execute("CREATE TABLE IF NOT EXISTS Domains(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(50), IP VARCHAR(25), Resolving VARCHAR(25), Server VARCHAR(60))")
#    cur.execute("""INSERT INTO Domains(Name, IP, Resolving, Server) VALUES(%s, %s, %s, 'Server Beach')""", (host, index, output))
# End mysql database insert

    #cur = con.cursor()
    #cur.execute("Update Domains set Problem='0' Where Name = %s", (host))
   else:
    #cur2 = con.cursor()

# Insert Domains into Mysql Database
#    cur.execute("INSERT INTO Domains(Name, IP, Resolving, Server, Problem) VALUES(%s, %s, %s, 'Problem', '1')", (host, index, output))
# End Insert Domains into Mysql Database

    #cur2.execute("Update Domains set Problem=1 Where Name = %s", (host))
    print colored(host, 'white'),colored(index, 'red'), colored(output, 'red'), colored(now.strftime("%Y-%m-%d"), 'white')
    z = open('failed', 'a')
    z.write(host + " old ip : " + index + " new ip : " + output)
    z.write('\n')
    z.close()
  except:
   print "Error" , host
   f = open('siteserror','a')
#   f.write(host + " ==>> " + "SERVER IP:  " + index)
   f.write(host)
   f.write('\n')
import sys
sys.stdin = open ('sitesok', 'r')
data = sys.stdin.readlines()
print "Domains : ", colored(len(data), 'red'), "domains"
sys.stdin = open ('failed', 'r')
data = sys.stdin.readlines()
print "Error resolving : ", colored(len(data), 'white'), "failed domains"

#import subprocess
#process = subprocess.Popen(['/root/niki/starter'], shell=True, executable="/bin/bash")
#output = process.communicate()[0]


#import smtplib
#from email.mime.text import MIMEText

#fp = open('/root/niki/checkfailed', 'r')
#msg = MIMEText(fp.read())
#fp.close()
#msg['Subject'] = 'Web site ip monitoring Warning'
#msg['From'] = 'monitor@sitedxr.com'
#msg['To'] = 'itsupport@1stonlinesolutions.com'

#toaddr = "hdimitrov@1stonlinesolutions.co.uk"
#cc = ['itsupport@1stonlinesolutions.com']
#toaddrs = [toaddr] + cc



#s = smtplib.SMTP('localhost')
#s.set_debuglevel(True)
#s.sendmail('monitor@sitedxr.com', toaddrs, msg.as_string())
#s.quit()

