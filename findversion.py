#!/usr/bin/python3
# File: findversion.py
# Author: bgstack15@gmail.com
# Startdate: 2016-10-31
# Title: Script that Displays Files and Version Numbers
# Purpose: To show the available version numbers of a file
# History:
# Usage:
#    findversion.py scrub.py /home/work
#    findversion.py [--dir] /home/work [--filename] scrub.sh
# Reference:
#    regex search http://stackoverflow.com/a/10477490
#    regex https://docs.python.org/3/howto/regex.html
#    manipulating dict https://docs.python.org/2/library/stdtypes.html#dict
#    parser from updateval.py 
#     and also https://docs.python.org/3/library/argparse.html#formatter-class
# Improve:
#    Make option for "newestonly" which just does "tail -n1"

import os, re, argparse, textwrap

findversionpyversion = "2016-11-01a"

# DEFINE FUNCTIONS

def isValidFile(_thisstring):
   # return true if not png, tgz, or other non-text file
   _isValidFile=True
   if re.compile('.*\.(tgz|png|gif|jpg|pyc|pyo|git|swp)').match(_thisstring):
      _isValidFile = False
   elif os.path.islink(_thisstring):
      _isValidFile = False
   #print( _thisstring + ": " + str(_isValidFile) )
   return _isValidFile

# EXAMPLE VARIABLE VALUES
searchdir = "/home/work/rpmbuild/SOURCES"
searchfile = "updateval.py"
newestonly = False

# DEFINE PARAMETERS
parser = argparse.ArgumentParser(
   description="Finds and displays a file for each unique version number.",
   formatter_class=argparse.RawDescriptionHelpFormatter,
   epilog=textwrap.dedent('''\
   Valid options include:
      ./findversion.py scrub.py /home/work
      ./findversion.py [--dir] /home/work [--filename] scrub.sh''') )
parser.add_argument("dir", nargs='?', default="NONE", help=argparse.SUPPRESS)
parser.add_argument("filename", nargs='?', default="NONE", help=argparse.SUPPRESS)
parser.add_argument("-d","--dir", default="NONE", help="the -d is optional")
parser.add_argument("-f","--filename", default="NONE", help="the -f is optional")
parser.add_argument("-V","--version", action="version", version="%(prog)s " + findversionpyversion)
parser.add_argument("-s","--string", default="NONE", help="exact string to put before version= search expression. Default is filename without punctuation.")

# PARSE PARAMETERS
args = parser.parse_args()
if args.dir == "NONE" and args.filename == "NONE":
   # throw an error, because nothing was defined
   # unless we want to force it to check all versions everywhere
   parser.parse_args(['-h'])
elif args.dir == "NONE":
   # use current directory
   if os.path.isdir(args.filename):
      searchdir = args.filename
      filename = "*"
   else:
      searchdir = os.getcwd()
      filename = args.dir
elif args.filename == "NONE":
   if os.path.isdir(args.dir):
      searchdir = args.dir
      filename = "*"
   else:
      searchdir = os.getcwd()
      filename = args.dir
else:
   if os.path.isdir(args.dir):
      searchdir = args.dir
      filename = args.filename
   else:
      if os.path.isdir(args.filename):
         searchdir = args.filename
         filename = args.dir
      else:
         print("Invalid directory: %s" % args.dir)
         quit()

searchfile = filename
if args.string == "NONE":
   searchstring = re.sub("[^a-zA-Z0-9]", "", searchfile)
else:
   searchstring = args.string

pattern = re.compile(r'.*' + searchstring + r'(py|sh)?version ?= ?(?P<quot>[\"\'])[0-9]{4}(-[0-9]{2}){2}[a-zA-Z](?P=quot)')
allversions = dict()

# DEBUG SECTION
if False:
   print("searchdir %s" % searchdir)
   print("searchfile %s" % searchfile)
   print("searchstring %s" % searchstring)

# PERFORM SEARCH HERE
for rootdir, subdirs, files in os.walk(searchdir):
   for filename in files:
      thispath = os.path.join(rootdir, filename)
      #print("file: " + thispath)
      if isValidFile(thispath):
         for i, line in enumerate(open(thispath)):
            for match in re.finditer(pattern, line):
               #print('%s: %s: %s' % (thispath, i+1, match.group() ))
               # get just version string
               thisversion = re.sub( r'.*([0-9]{4}(-[0-9]{2}){2}[a-zA-Z]).*', r'\1', match.group())
               #print("%s: %s" % (thisversion, thispath))
               allversions[thisversion] = thispath

# DISPLAY SORTED AND UNIQUE VERSION NUMBER WITH FILENAME
for item in sorted(allversions):
   print(str(item) + ": " + allversions[item])
