#!/usr/bin/python

from __future__ import print_function
import string, re
from appscript import *
import musicbrainzngs as m
import nltk
import optparse

m.set_useragent(
    "application",
    "0.1",
    "https://github.com/alastair/python-musicbrainz-ngs/",
)

verbose = True
        
def getinfo( release, song, album, artist ):
    ac = release['artist-credit']
    rl = release['release-list']
        
    newartist = release['artist-credit'][0]['artist']['name']
    
    distance = nltk.metrics.edit_distance(newartist, artist)
    if  ( distance > 5 ):
        if verbose:
            print(u"     ## Wrong artist: {}".format(newartist))
        return (release['title'],newartist,"",9999)

    distance = nltk.metrics.edit_distance(song, release['title']) 
    if  ( distance > 5):
        if verbose:
            print(u"     ## Wrong song: {}".format(release['title']))
        return (release['title'],newartist,"",9999)
               
    newsong = release['title']
    
    lowestDate = 9999
    bestAlbum = ""
    
    for a in rl:
        newalbum =a['title']
        if ('date' in a ):
            newdate = int(a['date'][:4])
        else:
            newdate = 9998
        
        #print(u"     {} in {} by {}  on {}".format( newsong, newalbum, newartist, newdate) )
        
        if (lowestDate > newdate):
            lowestDate = newdate
            bestAlbum = newalbum
            
    return (newsong, newartist, newalbum, newdate)

def handle_data( dict ) :
    if verbose:
            print (u"{} in {} by {}".format(dict['song'], dict['album'], dict['artist'] ) )
    
    result = m.search_recordings(artist = dict['artist'], recording=dict['song'], country='US', limit=15)
    
    lowestDate = 9999
    bestAlbum = dict['album']
    bestArtist = dict['artist']
    
    for (idx, release) in enumerate(result['recording-list']):
        (newsong, newartist, newalbum, newdate) = getinfo( release, dict['song'], dict['album'], dict['artist']  )
        if (lowestDate > newdate):
            lowestDate = newdate
            bestAlbum = newalbum
            bestArtist = newartist
            
        if verbose:
            print(u"     {} in {} by {}  on {}".format( newsong, newalbum, newartist, newdate) ) 

    if verbose:
            print()
    if verbose:
            print(u"----{} in {} by {}  on {}".format( dict['song'], bestAlbum, bestArtist, lowestDate) ) 
    return (dict['song'], bestAlbum, bestArtist, lowestDate)
    
def fix_itunes_names(fix=False):
    iTunes = app(u'/Applications/iTunes.app')
    selection = iTunes.windows[1].selection.get()
    dict = {}
    
    for track in selection:
        song =track.name()
        album = track.album()
        artist = track.artist()
        
        dict = {'artist': artist, 'album': album, 'song':song }
        
        try:
            (newsong, newalbum, newartist, newdate) =  handle_data( dict )
        
            if (fix == False ):
                continue
        
            track.name.set( newsong )
            track.album.set( newalbum )
            track.artist.set( newartist )
            track.year.set( newdate )
        except:
            continue
            
if __name__ == '__main__':
    option_parser = optparse.OptionParser(usage='%prog [apply]')
    options, args = option_parser.parse_args()
    
    if (len(args) > 0):
            verbose = False
            fix_itunes_names( True )
            
    else:
            fix_itunes_names( False )
        
