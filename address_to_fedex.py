#!/usr/bin/python

## address_to_fedex.py
##-------------------------------------------------------------------------
## We simply iterate through the selected contacts in Address Book.  For 
## each contact we fill out a dictionary based upon the contact's field
## values.  We then call fill_safari() from the module paste_to_fedex.py
## which must be in the same directory or in the Python path.


import string, sys, time, shutil
from appscript import *
import os
import paste_to_fedex
            
def process_ab_selection():
    
    AB = app(u'/Applications/Contacts.app')
    
    clients = AB.selection.get()
    
    order_data = {}    
    for client in clients:
        # normally this will only run once but I figured I'd make it so you can do more than one person
        
        order_data['last'] = client.last_name.get()
        if order_data['last'] == k.missing_value:
            order_data['last'] = ""
            
        order_data['first'] = client.first_name.get()
        if order_data['first'] == k.missing_value:
            order_data['first'] = ""
            
        order_data['company'] = client.name.get()
        if order_data['company'] == k.missing_value:
            order_data['company'] = "Unknown"
                    
        
        order_data['address'] = client.addresses.get()[0].street.get()
        if order_data['address'] == k.missing_value:
            order_data['address'] = ""
            
        order_data['city'] = client.addresses.get()[0].city.get()
        if order_data['city'] == k.missing_value:
            order_data['city'] = ""
            
        order_data['state'] = client.addresses.get()[0].state.get()
        if order_data['state'] == k.missing_value:
            order_data['state'] = ""
            
        order_data['zip'] = client.addresses.get()[0].zip.get()
        if order_data['zip'] == k.missing_value:
            order_data['zip'] = ""
        
        try:
        
            order_data['telephone'] = client.phones.items[1].value.get()
            if order_data['telephone'] == k.missing_value:
                order_data['telephone'] = "801-655-1996"
        except:
            order_data['telephone'] = "801-655-1996"
            
                      
        paste_to_fedex.fill_safari( order_data )
    
if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        process_ab_selection()
        

    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    