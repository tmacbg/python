#!/usr/bin/python
import sys
import signal


class TimeoutException(Exception):
  pass

from socket import gethostbyname
with open('/root/netwiselist1.csv') as input:
   for line in input:
    host, index = line.strip().split(';')
#    host = input.readlines()
    try:
#     output = gethostbyaddr(host)
     output = socket.gethostbyname(host)
#     check2 = str("%s %s => %s/%s" % (index, host, output[0], output[2]))
     check2 = str(output)
     f = open('checknetwise','a')
     f.write(check2)
     f.write('\n')
    except TimeoutException:
     print ""
    except:
     print host, "not found"
    
