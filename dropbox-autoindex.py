#!/usr/bin/env python2
#-*- coding: utf8 -*-

import os
import sys
import re
import argparse

base_url = "http://dl.dropbox.com/u"

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


def parse_arguments():
    """parse command line arguments"""
    parser = argparse.ArgumentParser(
            prog = 'dropbox-autoindex',
            description="Small and simple utility that automates index \
                         generation for dropbox public folder ")

    parser.add_argument('--version', action='version', version='%(prog)s 0.5')

    parser.add_argument('-p', '--public', default='~/Dropbox/Public',
        help='path to dropbox public folder')

    parser.add_argument('--index', default='index.html',
        help='filename of index file')

    parser.add_argument('--title', default='my dropbox',
        help='html title')

    parser.add_argument('-t', '--template',
        help='path to template file')

    parser.add_argument('-v', '--verbose', action='store_true', default=False,
        help='explain what is being done')

    parser.add_argument('-i', '--interactive', action='store_true',
        default=False, help='prompt before overwrite')

    parser.add_argument('-x', '--exclude', nargs='*', default=[],
        help='exclude files/folders from html')

    parser.add_argument('uid',
        help='dropbox user id')

    return parser.parse_args()


def build_index(html, path):
    """Replace special tags in template files and save as html files.

    Keyword arguments:
    html -- the code to replace the listing tag of the template
    path -- path to save the html file

    """
    html_file = os.path.join(path, arg.index)
    if prompt_overwrite(html_file) is False:
        vprint("=> Skipping...")
        return

    builder = re.compile("{% listing %}", re.I)
    contents = builder.sub(''.join(html), arg.template)

    fp = open(html_file, 'w')
    fp.write(contents)
    fp.close()

    vprint("=> Generated %s for folder '%s'." % (arg.index, path))


def traverse_path(cwd, parent=[]):
    """Recursively traverse dropbox public dir and generate html files

    Keyword arguments:
    cwd -- current working directory, traverse this path for files and folders
    parent -- list of parent folder names (default: [])

    """

    html = []
    vprint("Inspecting folder %s ..." % cwd)

    # create the "back" button
    if len(parent) > 0:
        html.append("""<li><a href="%s/%s/%s/%s">..</a></li> """ %
                (base_url, arg.uid, '/'.join(parent[:-1]), arg.index))

    for item in os.listdir(cwd):
        # ignore files/folders matching entries in exclude list
        if item in arg.exclude:
            continue

        full_path = os.path.join(cwd, item)

        if os.path.isdir(full_path):
            parent.append(item)
            html.append("""<li><a href="%s/%s/%s/%s">%s</a></li>""" %
                    (base_url, arg.uid, '/'.join(parent), arg.index, item))
            traverse_path(full_path, parent)
            parent.pop()

        else:
            html.append("""<li><a href="%s/%s/%s/%s">%s</a></li>""" %
                    (base_url, arg.uid, '/'.join(parent), item, item))

    build_index(html, cwd)
    return True


#---[ main ]----------------------------------------------------------------

# parse from command line
arg = parse_arguments()

# print only if verbose flag is set (http://bit.ly/p8Tckd)
if arg.verbose:
    def vprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
           print arg,
        print
else:
    vprint = lambda *a: None      # do-nothing function


# prompt user before overwritting index files in interactive mode
if arg.interactive:
    def prompt_overwrite(f):
        """Prompt user to overwrite file in given path."""
        if os.path.exists(f):
            while True:
                sys.stdout.write("File exists, overwrite? [y/n/q]: ")
                choice = raw_input().lower()
                if choice in ('y', 'yes'):
                    return True
                elif choice in ('n', 'no'):
                    return False
                elif choice in ('q', 'quit'):
                    vprint("Quit...")
                    sys.exit(1)
        else:
            return True
else:
    def prompt_overwrite(f):
        return True

# generate dropbox public directory
public_dir = os.path.abspath(os.path.expanduser(arg.public))

# exclude the index files and dropbox special file
arg.exclude.append(arg.index)
arg.exclude.append('.dropbox')

if arg.template is None:
    arg.template = template

# walk dropbox public folder and generate the html files
traverse_path(public_dir)

sys.exit(0)
