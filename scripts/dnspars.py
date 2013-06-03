#!/usr/bin/env python

import dpkt, socket, sys

if len(sys.argv) < 2 or len(sys.argv) > 2:
 print "Usage:\n", sys.argv[0], "filename.pcap"
 sys.exit()

f = open(sys.argv[1])
pcap = dpkt.pcap.Reader(f)

for ts, buf in pcap:
 try: eth = dpkt.ethernet.Ethernet(buf)
 except: continue
 if eth.type != 2048: continue
 try: ip = eth.data
 except: continue
 if ip.p != 17: continue
 try: udp = ip.data
 except: continue
 if udp.sport != 53 and udp.dport != 53: continue
 try: dns = dpkt.dns.DNS(udp.data)
 except: continue
 if dns.qr != dpkt.dns.DNS_R: continue
 if dns.opcode != dpkt.dns.DNS_QUERY: continue
 if dns.rcode != dpkt.dns.DNS_RCODE_NOERR: continue
 if len(dns.an) < 1: continue
 for answer in dns.an:
   if answer.type == 5:
     print "CNAME request", answer.name, "\tresponse", answer.cname
   elif answer.type == 1:
     print "A request", answer.name, "\tresponse", socket.inet_ntoa(answer.rdata)
   elif answer.type == 12:
     print "PTR request", answer.name, "\tresponse", answer.ptrname
