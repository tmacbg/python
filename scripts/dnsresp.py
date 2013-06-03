#!/usr/bin/python


# Requires pydns module: 
from datetime import datetime
import sys
import DNS
 
# Verify arguments
if len(sys.argv) != 3:
    print 'Usage: query_dns_server.py <Hostname> <DNS Server>'
    sys.exit(3)
 
hostname = sys.argv[1]
dns_server = sys.argv[2]
 
try:
    start = datetime.now()
 
    # Perform the DNS query
    s = DNS.Request(name=hostname, server=dns_server)
    resolve = s.req().answers
 
    end = datetime.now()
except DNS.Base.TimeoutError:
    print "Timeout from DNS server '%s'." % dns_server
    sys.exit(2)
 
millisec = (end - start).microseconds / 1000
print "Hostname '%s' was%s found via DNS server '%s'. Latency: %sms|'Latency(MS)'=%ms;;;" % (
    hostname,
    '' if resolve else ' not'
#    dns_server,
#    millisec,
#    millisec,
)
sys.exit(0) if resolve else sys.exit(2)
