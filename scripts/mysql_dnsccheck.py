#!/usr/bin/python


import datetime
import sys
import MySQLdb as mdb
from socket import gethostbyname
from termcolor import colored

con = mdb.connect('localhost', 'testuser', 'test123', 'testdb');

with con:

 with open('/root/biggest.csv') as input:
  for line in input:
   host, index = line.strip().split(',')
   now = datetime.datetime.now()
   cur = con.cursor()
   cur.execute("CREATE TABLE IF NOT EXISTS Domains(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(50), IP VARCHAR(25), Resolving VARCHAR(25))")
   cur.execute("""INSERT INTO Domains(Name, IP) VALUES(%s, %s)""", (host, index))

   try:
    output = gethostbyname(host)
    if output == index:
     print colored(host,'red'),colored(output,'green')
    else:
     print colored(host, 'white'),colored(index, 'red'), colored(output, 'red'), colored(now.strftime("%Y-%m-%d"), 'white')
     now1 = now.strftime("%Y-%m-%d %H:%M")
     cur.execute("UPDATE Domains SET Resolving = %s WHERE Name = %s", (output, host)) 
   except: 
     print "Error" , host
     f = open('checkseohostingerror','a')
     f.write(host + " ==>> " + "SERVER IP:  " + index)
     f.write('\n')

