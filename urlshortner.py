#!/usr/bin/python
# -*- coding: utf-8 -*-

### urlshortner.py
##
## Takes the front Safari window/tab and gets a bitly shortened url which
## it puts on the clipboard.
##
## I typically use this with a paste command in Wedge or Tweetbot so that I 
## can paste a short url but keep track of it with Bitly. In Quickeys I assign
## it to ctrl-v and then add in a cmd-v as part of the macro.
##
## It requires appscript to work. To install appscript type the following at
## the command line:
## sudo easy_install appscript
##
## It also requires you have a bitly username and API key. The ones below are
## not valid.

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


def shortenSafari():
    Safari = app(u'/Applications/Safari.app')
    url = Safari.windows[1].current_tab.URL.get()

    print url

    short_url = shorten(url)

    sa = OSAX()
    sa.set_the_clipboard_to(short_url)
    print short_url


if __name__ == '__main__':
    shortenSafari()
    sys.exit(0)
