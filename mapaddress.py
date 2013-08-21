#!/usr/bin/python

###############################
# mapaddress.py
###############################
#
# Brings up a dialog box prompting for a city and state.  It then queries
# the address book for all addresses within 75 miles.  (This value can be
# changed in the global constant "distance")
#
# The data is then opened up in a new document within TextMate or alternatively
# within TextEdit.  (The TextEdit code is present but commented out)

import urllib
from math import *
from appscript import *
import subprocess, sys

import osax
from time import sleep
from operator import itemgetter

key = "ABQIAAAAiyrScXyPkh5q77jH8M4DHRRn4uOMT5j2xtM4re-0wWy9Rxb7jRRJGH7C_xJQS37k6EJbze0Y598Y0g"

distance = 75
output_text = []
debug_script = False

def send_output(t):
    global output_text
    output_text.append(t)
    
def finish_send():
    global output_text
           
    # To send to TextMate
    #proc = subprocess.Popen(['mate'], shell=True, stdin=subprocess.PIPE)
    #proc.communicate(u'\n'.join(output_text))
    
    # To send to TextEdit
    app(u'TextEdit').make(new=k.document, with_properties={k.text: '\n'.join(output_text)})
    
    
    
def sigdigits(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
 
    # Use %e format to get the n most significant digits, as a string.
    format = "%." + str(n-1) + "e"
    r = format % x
    return float(r)


def deg2rad( pos ):
    return  [ float( pos[0] ) * 2 * pi / 360 , float( pos[1] ) * 2 * pi / 360 ]

def find_distance(co1, co2):
    """Given two coordinates (latitute, longitude) in degrees returns the distance
    beteween them."""
    
    try:
        co1 = deg2rad( co1 )
        co2 = deg2rad( co2 )
        earth = 3956.6 # radius of earth in miles
        d = acos( cos( co1[0] ) * cos( co1[1] ) * cos( co2[0] ) * cos( co2[1] ) + cos( co1[0] ) * sin( co1[1] ) * cos( co2[0] ) * sin( co2[1]) + sin( co1[0] ) * sin( co2[0] ) )  * earth
        return sigdigits(d,2) 
    except:
        return None
    
    
def get_location( query, key=key ): 
    """Get the ( latitute, longitude ) coordinates in radians corresponding to the query.
    If something goes wrong return None."""
        
    params = { }
    params[ 'key' ] = key
    params[ 'output' ] = 'csv'
    params[ 'q' ] = query
    
    params = urllib.urlencode( params )
    

    try:
        f = urllib.urlopen( "http://maps.google.com/maps/geo?%s" % params )
    except IOError:
        # maybe some local problem at google? let's try again
        sleep( 5 )
        try:
            f = urllib.urlopen( "http://maps.google.com/maps/geo?%s" % params )
        except IOError:
            # okay we give up
            return None
    
    response = f.read( ).split(',')
    f.close( )
    
    try:
        status = response[0]
        accuracy = response[1]
        latitude = response[2]
        longitude = response[3]
    except:
        return None
    
    if status != '200':
        return None
    else:
        return latitude, longitude

def scan_addresses( center, range ):
    
    AB = app('/Applications/Contacts.app')
    
    # uncomment below to search all people in Address Book
    # people = AB.people.get()
    
    # uncomment below to search for all people in specified group
    people = AB.groups[u'Clients'].people.get()
    
    address_list = []
    
    for person in people:
                
        if len(person.addresses()) > 0:
            
            try:
                address = (person.addresses())[0].street() + " "
                address = address + (person.addresses())[0].city() + " "
                address = address + (person.addresses())[0].state() + " "
                address = address + (person.addresses())[0].zip()

                loc = get_location( address )
                
                if loc == None:
                    continue
                    
                distance = find_distance( center, loc )
                
                if distance < range:
                    
                    if debug_script:
                        send_output("")
                        send_output(person.name())
                        send_output(address)
                        send_output( "Distance:" + str(distance))
                    
                    store = {}
                    store['name'] = person.name()
                    store['address'] = address
                    
                    if len(person.phones()) >0:
                        store["phone"] = person.phones()[0].value()
                    else:
                        store["phone"] = ""
                        
                    store['distance'] = distance
                        
                    address_list.append(store)
                    
            except:
                #print "error"
                continue
                
    return sorted(address_list, key=itemgetter('name'))

def fillnumbers( table, row, data):
   
    
    table.columns[1].cells[row].value.set( row )
    table.columns[2].cells[row].value.set( data["name"] )
    table.columns[3].cells[row].value.set( data["address"] )
    table.columns[4].cells[row].value.set( data["phone"] )
    table.columns[5].cells[row].value.set( str(data["distance"] ))
    
    
def addresses_to_numbers(center="Provo, UT", range=50):
    
    list = scan_addresses( center, range )
    
    # Hack to create new document in numbers
    
    app(u'Numbers').activate()
    app(u'System Events').processes[its.title == u'Numbers'].processes[1].menu_bars[1].menu_bar_items[3].menus[1].menu_items[1].click()
    
    table = app(u'Numbers').documents[1].sheets[1].tables[1]
    
    # do a header
    fillnumbers( table, 1, {'name':'Name', 'address':'Address', 'phone':'Phone', 'distance':'Distance'})
    
    row = 2
    for l in list:
        fillnumbers( table, row, l)
        row = row + 1
        
def list_addresses(center="Provo, UT", range=50):
    
    list = scan_addresses( center, range )
    send_output( "Lists")
    send_output( "------")
    
    for l in list:
        send_output(l['name'])
        send_output(l['address'])
        send_output(l['phone'])
        send_output("Distance:  " + str(l['distance']))
        send_output('\n')
        
def get_center():
    
    AB = app('/Applications/Address Book.app')
    a = AB.selection.get()[0]

    send_output("Searching around " + a.name())
    
    address = a.addresses()[0].street() + " "
    address = address + a.addresses()[0].city() + " "
    address = address + a.addresses()[0].state() + " "
    address = address + a.addresses()[0].zip()
    
    send_output( address )
    
    loc = get_location( address )
    
    return loc

def make_center(address):
    send_output("Search around " + address)
    
    loc = get_location( address )
    
    return loc
    
def test_ab():
    AB = app('/Applications/Address Book.app')
    members = AB.groups[u'Clients'].people.get()
    for m in members:
        print m.name()
        
def main():

    global distance

    if len( sys.argv ) > 2:
        q = sys.argv[1]
        center = get_location( q )
        distance = sys.argv[2]
        
    else:
        #center = get_center()
        sa = osax.OSAX()
        results = sa.display_dialog("Search Around: ", with_title="Area Search",  default_answer="los angeles, ca")
        if results[k.button_returned] == u"OK":
            center = make_center(results[k.text_returned])
            

        
    if center == None:
        send_output("Address is bad")
      
    # addresses_to_numbers( center, distance )  
    list_addresses(center, distance)
    finish_send()


if __name__ == '__main__':
    
    main()
    
