#!/usr/bin/python

## paste_to_fedex.py
##-------------------------------------------------------------------------
## Given a dictionary with address information [see test() for fields] this
## opens up a new FedEx shipping window in Safari and fills in the 
## appropriate fields.  Run by itself this simply fills FedEX with test data.
## This is primarily intended to be a module called by other scripts.

import string, sys, time, shutil
from appscript import *
import os

# Checks to see if we need to login to FedEx
        
def check_FedEx_login():

    try:
        expected_text = "https://www.fedex.com/shipping/shipEntryAction"
        s = app(u'/System/Library/CoreServices/System Events.app').application_processes[u'Safari'].windows[1].static_texts[1].name.get(resulttype=k.unicode_text)
 
        if expected_text in s:
            return
    except:
        time.sleep(1)
        
    name = "name"
    passwd = "pass"
    
    Safari = app(u'/Applications/Safari.app')
    FEdoc = Safari.documents[0].get()
    Safari.do_JavaScript("document.forms['logonForm']['username'].value = '" + name + "'", in_=FEdoc)
    Safari.do_JavaScript("document.forms['logonForm']['password'].value = '" + passwd + "'", in_=FEdoc)
    Safari.do_JavaScript("document.forms['logonForm'].submit()", in_=FEdoc)
    #time.sleep(3)

    
## This checks to see if Safari is finished loading the FedEx page

def check_Safari_done():
    
    check_FedEx_login()
    
    """Waits for Safari to stop loading"""
    
    while True:
        try: 
            s = app(u'Safari').documents[1].source.get()
            break
        except:
            # don't even have enough page information to get the source
            time.sleep(1)
            continue
        
    while True:
        try:
            s = app(u'Safari').documents[1].source.get()
            if "</html>" in s[-10:].lower():
                break
        except:
            time.sleep(1)
            break


## This does all the work of actually filling in the Safari fields for the FedEx website.
## It is pretty self-explanatory.  We check to see if the page is finished loading
## (see check_Safari_done above) and then simply use Javascript to fill in the fields.
## We selected the fields by simply browsing the source HTML for the FedEx page.
##
## Beyond that we simply do a little error checking on company and phone fields, putting
## in some defaults.
##
## We fill in some defaults that you might wish to change, such as the box weight.

def fill_safari( order_data ):

    Safari = app(u'/Applications/Safari.app')
    Safari.activate()
    
    ## make a new window and go to the FedEx site.  (Note: you have to have logged in already)
    Safari.make(new=k.document)
    Safari.documents[0].URL.set(u'https://www.fedex.com/shipping/shipAction.do?method=doInitialize&urlparams=us')
    
    ## get the document name we just created -- we use that to make sure we operate on the right windo
    
    check_Safari_done()
    
    time.sleep(3)
    
    FEdoc = Safari.documents[0].get()        
    
    if order_data["telephone"] == None:
        order_data["telephone"] = "801-655-1996"
        
    if order_data["telephone"] == "":
        order_data["telephone"] = "801-655-1996"
            
    if order_data["company"] == None:    
        order_data["company"] = "---"
        
    if order_data["company"] =="":
        order_data["company"] == "---"
        
    if 'weight' not in order_data:
        weight = '1'
    else:
        weight = str(order_data['weight'])
        
    if 'value' not in order_data:
        boxvalue = "0"
    else:
        boxvalue = str(order_data['value'])
        
    if 'shipping' not in order_data:
        shipping = 'FedEx Ground'
    else:
        shipping = order_data['shipping']
 
    # the field for residential has to be "true" or "false"
    
    if 'residential' not in order_data:
        residential = 'false'
    else:
        residential = order_data['residential']
        
        
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.companyName'].value = \"" + order_data['company'] + "\"", in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.contactName'].value = '" + order_data["first"] + ' ' + order_data["last"] + "'" , in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['toData.addressLine1'].value = '" + order_data["address"] + "'", in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['toData.city'].value = '" + order_data["city"] + "'",  in_=FEdoc)
    
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.stateProvinceCode'].value = '" + order_data["state"] + "'",  in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['toData.zipPostalCode'].value = '" + order_data["zip"] + "'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.phoneNumber'].value = '" + order_data["telephone"] + "'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.residential'].checked = " + residential,  in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['psdData.serviceType'].value = '" + shipping + "'" ,  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psdData.packageType'].value = 'Your Packaging'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psd.mps.row.weight.0'].value = '" + weight + "'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psd.mps.row.dimensions.0'].value = '1006956'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psd.mps.row.declaredValue.0'].value = '" + boxvalue + "'",  in_=FEdoc)
    Safari.do_JavaScript("recipientAddressChanged()",  in_=FEdoc)

    return
    

## Module unit test    
        
def test():
    # our unit test
    order_data = {}
    order_data['first'] = "Clark"
    order_data['last'] = "Goble"
    order_data['company'] = "Amano "
    order_data['address'] = "Some Street"
    order_data['city'] = "Sometown"
    order_data['state'] = "UT"
    order_data['zip'] = "11111"
    order_data['telephone'] = "801-111-1111"
    
    fill_safari( order_data )
    
    
if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        test( )
        

    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    