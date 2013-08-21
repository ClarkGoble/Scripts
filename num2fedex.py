#!/usr/bin/python

## Puts the selected addresses from Address Book into Numbers

from appscript import *
import sys
import time

def check_Safari_done():

    time.sleep(3)

def fill_safari( order_data ):

    print order_data
    Safari = app(u'/Applications/Safari.app')
    Safari.activate()
    
    ## make a new window and go to the FedEx site.  (Note: you have to have logged in already)
    Safari.make(new=k.document)
    Safari.documents[0].URL.set(u'https://www.fedex.com/shipping/shipAction.do?method=doInitialize&urlparams=us')
    
    ## get the document name we just created -- we use that to make sure we operate on the right windo
    
    check_Safari_done()
    
    time.sleep(1)
    
    FEdoc = Safari.documents[0].get()        
    
    if order_data["telephone"] == None:
        order_data["telephone"] = "801-655-1996"
        
    if order_data["telephone"] == "":
        order_data["telephone"] = "801-655-1996"
        
    print order_data["telephone"]
    

    if order_data["company"] == None:    
        order_data["company"] = "---"
        
    if order_data["company"] =="":
        order_data["company"] == "---"
        
        
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.companyName'].value = \"" + order_data['company'] + "\"", in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.contactName'].value = '" + order_data["name"] + "'" , in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['toData.addressLine1'].value = '" + order_data["address"] + "'", in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['toData.city'].value = '" + order_data["city"] + "'",  in_=FEdoc)
    
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.stateProvinceCode'].value = '" + order_data["state"] + "'",  in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['toData.zipPostalCode'].value = '" + order_data["zip"] + "'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.phoneNumber'].value = '" + order_data["telephone"] + "'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['toData.residential'].checked = false",  in_=FEdoc)

    Safari.do_JavaScript("document.forms['shipActionForm']['psdData.serviceType'].value = 'FedEx Ground'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psdData.packageType'].value = 'Your Packaging'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psd.mps.row.weight.0'].value = '2'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psd.mps.row.dimensions.0'].value = '1006956'",  in_=FEdoc)
    Safari.do_JavaScript("document.forms['shipActionForm']['psd.mps.row.declaredValue.0'].value = '0'",  in_=FEdoc)

    Safari.do_JavaScript("recipientAddressChanged()",  in_=FEdoc)

    return

def preparenumbers():
    app(u'Numbers')

def getnumbers( rownumber):
    
    ad = {}
    
    table = app(u'Numbers').documents[1].sheets[1].tables[1]
    

    ad["company"] = ""
    ad["row"] = table.columns[1].cells[rownumber].value.get()
    ad["name"] = table.columns[2].cells[rownumber].value.get()
    ad["address"] = table.columns[4].cells[rownumber].value.get()
    ad["city"] = table.columns[5].cells[rownumber].value.get()
    ad["state"] = table.columns[6].cells[rownumber].value.get()


    
    ad["zip"] = str(int(table.columns[7].cells[rownumber].value.get()))
    
    print type( ad['zip'])
    if type( ad["zip"] ) == float:
        print "B ", ad["zip"]
        ad["zip"] = str(int(ad["zip"]))
        print "A ", ad["zip"]
    else:
        print ad["zip"]
        
    ad["telephone"] = table.columns[8].cells[rownumber].value.get()

    return ad
    
def get_address():
     
    for row in range(2,38):
        address = getnumbers( row )
        print address
        fill_safari( address )
    
if __name__ == '__main__':
    
    get_address()
    
    # change to 0 for success, 1 for (partial) failure
    sys.exit(0) 
    