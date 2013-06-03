#!/usr/bin/python

# Send domains with changed ip addresses last 24H


import smtplib
from email.mime.text import MIMEText

text = 'path to text file'

fp = open('text', 'rb')
msg = MIMEText(fp.read())
fp.close()
msg['Subject'] = 'Web site ip monitoring Warning'
msg['From'] = 'monitor@sitedxr.com'
msg['To'] = 'itsupport@1stonlinesolutions.com'

s = smtplib.SMTP('178.16.129.106', 25)
s.sendmail('office@kotloni.info', 'nnedelchev@1stonlinesolutions.co.uk', msg.as_string())
s.quit()


