#!/usr/bin/env python


import re
from collections import defaultdict, namedtuple

format_pat= re.compile( 
    r"(?P<host>[\d\.]+)\s" 
    r"(?P<identity>\S*)\s" 
    r"(?P<user>\S*)\s"
    r"\[(?P<time>.*?)\]\s"
    r'"(?P<request>.*?)"\s'
    r"(?P<status>\d+)\s"
    r"(?P<bytes>\S*)\s"
    r'"(?P<referer>.*?)"\s' # [SIC]
    r'"(?P<user_agent>.*?)"\s*' 
)

Access = namedtuple('Access',
    ['host', 'identity', 'user', 'time', 'request',
    'status', 'bytes', 'referer', 'user_agent'] )

def access_iter( source_iter ):
    for log in source_iter:
        for line in (l.rstrip() for l in log):
            match= format_pat.match(line)
            if match:
                yield Access( **match.groupdict() )
