#!/usr/bin/env python2
#-*- coding: utf8 -*-

import os
import sys
import re

base_url = "http://dl.dropbox.com/u"
index_file = "index.html"
default_public = os.path.expanduser("~/Dropbox/Public")
uid = ""
ignore = ['.dropbox']

template = """<!DOCTYPE html>
<head>
   <meta http-equiv="content-type" content="text/html; charset=utf-8" />
   <title></title>
   <!-- <link rel="stylesheet" href="" type="text/css" media="screen"/> -->
</head>
<body>
  <div class="listing">
    <ul>
      {% listing %}
    </ul>
  </div>
</body>
</html>
"""


def build_index(template, html, path):
    builder = re.compile("{% listing %}", re.I)

    html_file = os.path.join(path, index_file)
    fp = open(html_file, 'w')

    contents = builder.sub(''.join(html), template)
    fp.write(contents)
    fp.close()


def traverse_path(cwd, parent=[]):
    html = []

    #cwd = os.path.abspath(cwd)

    #print 'inspecting folder %s' % cwd

    for item in os.listdir(cwd):
        #full_path = os.path.abspath(os.path.join(cwd, item))
        full_path = os.path.join(cwd, item)
        if os.path.isdir(full_path):
            parent.append(item)
            html.append("""<li><a href="%s/%s/%s/%s">%s</a></li>"""
                    % (base_url, uid, '/'.join(parent), index_file, item))
            traverse_path(full_path, parent)
            parent.pop()
        else:
            if item in ignore:
                continue
            #print '    found FILE with name %s' % item
            html.append("""<li><a href="%s/%s/%s/%s">%s</a></li>"""
                    % (base_url, uid, '/'.join(parent), item, item))

    #print 'DONE inspecting folder %s' % cwd
    #print
    build_index(template, html, cwd)
    #print "\n\n%s\n\n" % '\n'.join(html)

try:
    public_dir = os.path.abspath(os.path.expanduser(sys.argv[1]))
except:
    public_dir = default_public

traverse_path(public_dir)
sys.exit(0)

