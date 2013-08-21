#!/usr/bin/python

from appscript import *

def main():
    sw = app(u'Safari').windows[its.visible == True].get()
    for w in sw:
        w.index.set(1)  # move to front


if __name__ == '__main__':
    main()