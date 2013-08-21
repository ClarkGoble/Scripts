#!/usr/bin/env python
# -*- coding: utf-8 -*-

## tweetrepost.py
##--------------------
## Takes the currently selected tweet in Tweetbot, copies it to the clipboard, scrapes the 
## web data for it and generates a retweet that is then pasted into a new post window in
## Kiwi

from subprocess import PIPE, Popen
import urllib
import string, re, time
from bs4 import BeautifulSoup
import bitly_api
from osax import OSAX
from appscript import *

bitlyUserName = 'user'
bitlyAPIKey = 'key'

def shorten(url):
    """
    Given an url this creates and returns the bitly shortened url for it
    """

    bitly = bitly_api.Connection(bitlyUserName, bitlyAPIKey)
    try:
        short = bitly.shorten(url)
    except:
        # most errors are because it already exists as a link
        info = bitly.lookup(url)
        return info[0]['url']
    return short['url']



def setclipboard( text ):
    """
    Sets the clipboard to text
    """
    sa = OSAX()
    sa.set_the_clipboard_to( text )
    
    
def getclipbloard( ):
    """
    Returns as a string the data on the clipboard
    """
    
    sa = OSAX()
    return sa.the_clipboard() 
    
    
def  gettweet():
    """
    Gets the currently selected tweet from Tweetbot
    """
    
    app(u'Tweetbot').activate()
    app(u'System Events').keystroke(u'c', using=k.command_down)
    time.sleep(1)
    return getclipbloard()
        
def getretweet( source, post ):
    """
    Scrapes the web version of the current tweet returning  formatted retweet text
    """
    
    # get the HTML for the div tag with our tweet id
    soup = BeautifulSoup( source )
    hit = soup.find('div',attrs={'data-tweet-id':post})
    
    # get the username HTML within our div tag and then extract the name, prepending an
    # alternative to the @ symbol so it doesn't confuse people on ADN
    usertext = hit.find('strong',attrs={'class':'fullname js-action-profile-name show-popup-with-id'})
    username = usertext.get_text()
    username =  u"\u2672" + username.encode("utf-8")
        
    # get the tweet text also replacing any @ text with our ADN alternative character
    tweet = hit.find('p','js-tweet-text tweet-text')
    tweettext = tweet.get_text().replace(u"@", u"\u2672")
    
    links = tweet.find_all('a')
    
    if links != None:
        for l in links:
            if l.has_key('data-expanded-url'):
                flink = l['data-expanded-url']
                flink = shorten(flink)
                linktext = l.get_text()
                tweettext = tweettext.replace(linktext, flink)
                break
    
    tweettext = tweettext.replace(u"\u2026",u"")    # replace ending elipses
    
    return "Retweet quoting " + username + ": " + tweettext

def pasteretweet( ):
    """
    Creates a new message in Kiwi for ADN and then pastes the clipboard in
    """
    
    app(u'Kiwi').activate()
    app(u'System Events').keystroke(u'n', using=k.command_down)
    time.sleep(1)
    app(u'System Events').keystroke(u'v', using=k.command_down)
    return
        
def getpost(url):
    """
    Given an url to a Twitter tweet this returns the post number
    """
    
    try:
        lines = url.split("\n")
        l = lines[0].strip()
        match = re.match(r'https://twitter.com/.*/status/(\d+)', l)
        post = match.group(1)
    except:
        post = ""
        print "Invalid Format"
        
    return post

def main():
    url = gettweet()
    post = getpost(url)
    print post
    
    source= urllib.urlopen( url ).read()
    retweet = getretweet( source, post )
    setclipboard( retweet )
    pasteretweet( )

if __name__ == '__main__':
    main()

