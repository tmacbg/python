#!/usr/bin/env python

###############################################################################
# Copyright 2012 FastSoft Inc.
# Copyright 2012 Devin Anderson <danderson (at) fastsoft (dot) com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.  You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations under
# the License.
###############################################################################

from locale import LC_ALL, getlocale, setlocale
from optparse import OptionParser
from sys import stdout

from psinsights.service import Service

# This API key belongs to Devin Anderson (danderson@fastsoft.com).
API_KEY = "AIzaSyBDmdGLqKsT6kTXH205f34VGEeoSNPik2Y"

def compare_rules(data1, data2):
    return -cmp(data1[1].impact, data2[1].impact)

def main():
    setlocale(LC_ALL, '')
    parser = OptionParser("usage: %prog [options] url")
    parser.add_option("-l", "--locale", action="store", default=getlocale()[0],
                      dest="locale", help="Locale to use for analysis output")
    parser.add_option("-p", "--print-all-rules", action="store_true",
                      default=False, dest="print_all_rules",
                      help="Print all rules, including rules where URL "
                      "performs optimally")
    parser.add_option("-s", "--strategy", action="store",
                      default=Service.STRATEGY_DESKTOP, dest="strategy",
                      help="Analysis strategy ('desktop' or 'mobile')")
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error("incorrect number of required arguments")

    service = Service(API_KEY)
    url = args[0]
    analysis = service.analyze(url, options.locale, options.strategy)
    stats = analysis.statistics
    version = analysis.version

    stdout.write("URL: %s\n"
                 "Title: %s\n"
                 "Page Score: %s\n"
                 "Version: %s.%s\n\n"
                 "Total Resource Count: %s\n"
                 "Total Request Bytes: %s\n"
                 "Static Resource Count: %s\n"
                 "CSS Resource Count: %s\n"
                 "CSS Response Bytes: %s\n"
                 "Flash Response Bytes: %s\n"
                 "Host Count: %s\n"
                 "HTML Response Bytes: %s\n"
                 "Image Response Bytes: %s\n"
                 "JavaScript Resource Count: %s\n"
                 "JavaScript Response Bytes: %s\n"
                 "Text Response Bytes: %s\n"
                 "Other Response Bytes: %s\n" %
                 (url, analysis.title, analysis.score, version.major,
                  version.minor, stats.resource_count,
                  stats.total_request_bytes, stats.static_resource_count,
                  stats.css_resource_count, stats.css_response_bytes,
                  stats.flash_response_bytes, stats.host_count,
                  stats.html_response_bytes, stats.image_response_bytes,
                  stats.javascript_resource_count,
                  stats.javascript_response_bytes, stats.text_response_bytes,
                  stats.other_response_bytes))

    improve_rule_data = []
    optimal_rule_data = []
    for id, rule in analysis.results.rules.iteritems():
        if rule.score == 100:
            optimal_rule_data.append((id, rule))
        else:
            improve_rule_data.append((id, rule))

    if improve_rule_data:
        improve_rule_data.sort(compare_rules)
        stdout.write("\nHere are some improvements that can be made.\n")
        for i in xrange(len(improve_rule_data)):
            id, rule = improve_rule_data[i]
            stdout.write("\n%d.) %s\n"
                         "Id: %s\n"
                         "Score: %s\n"
                         "Impact: %s\n" %
                         (i + 1, rule.localized_name, id, rule.score,
                          rule.impact))
            for block in rule.url_blocks:
                stdout.write("\n%s\n" % unicode(block.header).strip())
                for url in block.urls:
                    stdout.write("\n\t%s\n" % unicode(url.result).strip())
                    for message in url.details:
                        stdout.write("\n\t%s\n" % unicode(message).strip())

    if options.print_all_rules and optimal_rule_data:
        stdout.write("\nHere are some cases where the page is performing "
                     "well.\n")
        for i in xrange(len(optimal_rule_data)):
            id, rule = optimal_rule_data[i]
            stdout.write("\n%d.) %s\n"
                         "Id: %s\n" % (i + 1, rule.localized_name, id))

if __name__ == "__main__":
    main()

