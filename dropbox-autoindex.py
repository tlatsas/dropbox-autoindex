#!/usr/bin/env python2
#-*- coding: utf8 -*-

import os
import sys
import re

base_url = "http://dl.dropbox.com/u"
index_file = "index.html"
default_public = os.path.expanduser("~/Dropbox/Public")
uid = "37339790"
ignore = ['.dropbox', index_file]

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
verbose = True

def build_index(template, html, path):
    builder = re.compile("{% listing %}", re.I)

    html_file = os.path.join(path, index_file)
    fp = open(html_file, 'w')

    contents = builder.sub(''.join(html), template)
    fp.write(contents)
    fp.close()


def traverse_path(cwd, parent=[]):
    html = []
    vprint("Inspecting folder %s ..." % cwd)

    if len(parent) > 0:
        html.append("""<li><a href="%s/%s/%s/%s">..</a></li> """ %
                (base_url, uid, '/'.join(parent[:-1]), index_file))

    for item in os.listdir(cwd):
        full_path = os.path.join(cwd, item)

        if os.path.isdir(full_path):
            parent.append(item)
            html.append("""<li><a href="%s/%s/%s/%s">%s</a></li>""" %
                    (base_url, uid, '/'.join(parent), index_file, item))
            traverse_path(full_path, parent)
            parent.pop()

        else:
            if item in ignore:
                continue
            html.append("""<li><a href="%s/%s/%s/%s">%s</a></li>""" %
                    (base_url, uid, '/'.join(parent), item, item))

    build_index(template, html, cwd)
    vprint("=> Generated %s for folder '%s'." % (index_file, cwd))
    return True


# print only if verbose flag is set (http://bit.ly/p8Tckd)
if verbose:
    def vprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
           print arg,
        print
else:
    vprint = lambda *a: None      # do-nothing function



try:
    public_dir = os.path.abspath(os.path.expanduser(sys.argv[1]))
except:
    public_dir = default_public

traverse_path(public_dir)
sys.exit(0)

