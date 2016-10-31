#!/usr/bin/python3
# File: findversion.py
# Author: bgstack15@gmail.com
# Startdate: 2016-10-31
# Title: Script that Displays Files and Version Numbers
# Purpose: To show the available version numbers of a file
# History:
# Usage:
#    findversion.py scrub.py /home/work
#    findversion.py [--dir] /home/work [--filename] scrub.sh [--newestonly]
# Reference:
#    regex search http://stackoverflow.com/a/10477490
#    regex https://docs.python.org/3/howto/regex.html
#    manipulating dict https://docs.python.org/2/library/stdtypes.html#dict
# Improve:

import os, re

findversionpyversion = "2016-10-31a"

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

# PREPARE VARIABLES
#searchstring = re.sub("[^a-zA-Z0-9]", "", searchfile)
searchstring = "updateval"
pattern = re.compile(r'.*' + searchstring + r'version ?= ?([\"\'])[0-9]{4}(-[0-9]{2}){2}[a-zA-Z]\1')
allversions = dict()

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
