#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import subprocess

# path to the openmeta binary

openmetapath = '/Users/clarkgoble/bin/openmeta'

# path "head" that is removed before assigning meta tags

headpath = '/Users/clarkgoble/documents/chocolate'

# path to update

updatepath = '/Users/clarkgoble/documents/chocolate'


def checkopenmeta():
    """
    Check to make sure the openmeta binary exists
    """

    return os.path.exists(openmetapath)


def openmeta(pathname, tags):
    """Given a filename and array of tags calls openmeta to tag
    the file with metadata
    """

    # get real pathname

    path = os.path.realpath(pathname)

    ar = [openmetapath, '-s']
    ar.extend(tags)
    ar.extend(['-p', path])

    # call the shell script

    print ar
    p = subprocess.Popen(ar, stdout=subprocess.PIPE)
    (stdout, stderr) = p.communicate()

    return stdout


def findinarray(array, words):
    """
    Search elements in an array for the array of words and return
    all elements in which the words is found
    """

    breaker = False
    found = []
    for w in words:
        for a in array:
            m = re.search(w, a)
            if m != None:
                found.append(w)
                breaker = True
                break
        if breaker:
            breaker = False
            break
    return found


def lookupname(name):
    """
    Given a name it checks to see if it is of the form
    'Company Name YY-MM-DD' and then extracts the date
    and company name if it is appropriate.
    """
    try:
        m = re.search("(\D+) ([0-9]+-[0-9]+-[0-9]+)", name)
        print 'Name: ', name
        print m.group(0)
        print m.group(1)
        if m == None:
            return None
    except:
        print 'Regex err: ', name
        return None

    print 'S: ', m.group(0), m.group(1)
    return [m.group(0), m.group(1)]


def tagsfromname(pathtags, name):
    """
    Given a set of path tags (each element is one element of path
    and a name this generates a set of tags by adding a tag for each
    path element, a tag for words that are looked up out of the path,
    and tags generated from the file name.
    """

    tags = pathtags
    words_to_search = ['Accounting', 'Awards', 'Amano', 'Lextek',
                       'label']

    found = findinarray(pathtags, words_to_search)
    tags.extend(found)

    nametags = lookupname( name )
    if nametags == None:
        return tags

    tags.extend( nametags )

    return tags


def quotedspaces(array):
    """
    Takes all the array elements that have spaces and returns a new array with
    those elements quoted.  I also remove duplicates at the same time.
    """

    n = []
    for a in array:
        if ' ' in a:
            n.append("'" + a + "'")
        else:
            n.append(a)
    return list(set(n))  # removes duplicates


def tag(filepath):
    """
    Tags the file pointed at by filepath by removing the headpath from it
    and treating each folder left as a separate tag.
    """

    shortpath = filepath[len(headpath):].split('/')
    pathtags = shortpath[:-1]
    name = shortpath[-1:]

    tags = quotedspaces(tagsfromname(pathtags, name[0]))
    print name, tags
    openmeta(filepath, tags)


def parsefolder(f=updatepath):
    """
    Given a folder path traverses it calling tag(file) for each
    file and recursively calling itself for each folder
    """

    try:
        files = os.listdir(f)

        for file in files:
            if file[0] == '.':
                continue

            filepath = f + '/' + file

            if os.path.isfile(filepath):
                tag(filepath)
                continue

            if os.path.isdir(filepath):
                parsefolder(filepath)
    except:
        print 'Error at: ' + filepath
        pass


def test():
    print openmeta('/Users/clarkgoble/Downloads/2011-08-31/openmeta-0.1.1dev/MANIFEST.in'
                   , ['a', 'b', 'c'])


def main():
    if not checkopenmeta():
        print "The openmeta binary doesn't exist at " + openemtapath
        sys.exit(-1)

    parsefolder()


if __name__ == '__main__':
    main()

    # change to 0 for success, 1 for (partial) failure

    sys.exit(0)
