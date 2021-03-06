#!/usr/bin/python
# -*- coding: utf-8 -*-

### URL Shortner for Reeder
### You must first set up the Copy Link service and assign it a ^C shortcut.

from appscript import *
import sys
import time
import bitly_api
from osax import OSAX

bitlyUserName = 'user'
bitlyAPIKey = 'key'


def shorten(url):
    bitly = bitly_api.Connection(bitlyUserName, bitlyAPIKey)
    short = bitly.shorten(url)
    return short['url']


def shortenReeder():
    Reeder = app(u'/Applications/Reeder.app')
    Reeder.activate()
    SE = app(u'System Events')
    SE.keystroke('c', using=k.control_down)
    
    sa = OSAX()
    url = sa.the_clipboard()

    print url

    short_url = shorten(url)
    sa.set_the_clipboard_to(short_url)
    
    print short_url


if __name__ == '__main__':
    shortenReeder()
    sys.exit(0)
