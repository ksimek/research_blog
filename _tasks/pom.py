#!/usr/bin/env python
from __future__ import print_function
import fileinput
from datetime import datetime

cur_year = 0;
cur_month = 0;
cur_day = 0;
cur_desc = '';

i = 0;

try:
    of = open('../pomodoro.md', 'w');
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
    exit(1);

print('---', file=of);
print('layout: page', file=of);
print('title: Pomodoro', file=of);
print('description: ""', file=of);
print('---', file=of);
print('{% include JB/setup %}', file=of);

print('Below is an automated list of my completed [Pomodoro sessions](http://en.wikipedia.org/wiki/Pomodoro_Technique).  I use the excellent Pomodoro app by Ugo Landini, which sadly appears to be no longer in development.  If anyone knows of a newer Pomodoro app with shell script automation, [let me know]({{site.baseurl}}/contact.html).\n\nThe list below only accounts for a fraction of my actual work -- many days I forego the Pomodoro technique entirely, or use it sparingly.', file=of);

# TODO: reversed dates, but forward times 
# TODO: one file per date, table of contents page, 
# Generator plugin to add "pomodoro_file_path" field to appropriate files
# modify post.html include to add pomodoro section at end of file.
# update "pomodoro_path" tag?
#for line in reversed(open("../pomodoro.txt").readlines()):
for line in open("../pomodoro.txt").readlines():
    i += 1;
    fields = line.split(None, 1);
    if len(fields) != 2:
        print("Record %d invalid", i)
    timestamp = int(fields[0].rstrip(':'));
    desc = fields[1].rstrip()

    if desc == cur_desc:
        desc = '"'

    dt = datetime.fromtimestamp(timestamp);

    # write date anchor tags
    if dt.year != cur_year:
        print('<a id="{:s}"></a>'.format(dt.strftime('%Y')), file=of);
        print('<a id="{:s}"></a>'.format(dt.strftime('%Y_%m')), file=of);
        print('<a id="{:s}"></a>'.format(dt.strftime('%Y_%m_%d')), file=of);
    elif dt.month != cur_month:
        print('<a id="{:s}"></a>'.format(dt.strftime('%Y_%m')), file=of);
        print('<a id="{:s}"></a>'.format(dt.strftime('%Y_%m_%d')), file=of);
    elif dt.day != cur_day:
        print('<a id="{:s}"></a>'.format(dt.strftime('%Y_%m_%d')), file=of);

    # write date title
    if dt.year != cur_year or dt.month != cur_month or dt.day != cur_day:
        print('##{:s}'.format(dt.strftime('%B %d, %Y')), file=of);

    # list accomplished tasks
    print('{:s} {:s}  '.format(dt.strftime('%X'), desc), file=of);

    cur_year = dt.year;
    cur_month = dt.month;
    cur_day = dt.day;
    cur_desc = desc;
