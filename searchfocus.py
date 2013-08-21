#!/usr/bin/python

from appscript import *

# our main javascript - tries to guess where the search text input widget is.

javascript = """
    var inputs = document.getElementsByTagName('input'),
        firstSearch = false,
        textinputs = [],
        i, t;
    for (i = 0; i < inputs.length; i++) 
        if (((inputs[i].type === 'text') || (inputs[i].type === 'search')) && inputs.disabled !== true) 
            textinputs.push(inputs[i]);
    for (t = 0; t < textinputs.length; t++) 
        if ((/search/i).test(textinputs[t].className) || 
        (/(^[sq]$|search|query)/i).test(textinputs[t].id) || 
        (/^(q(uery)?|s|.*?search.*)$/).test(textinputs[t].name)) {
            firstSearch = textinputs[t];
            break;
        }
    if (!firstSearch) 
        textinputs[0].focus();
    else 
        firstSearch.focus();
    """
    
# our custom javascript which selects the search input widget by ID

js_id = """document.getElementByID("{}").focus();"""

# global variables for appscript - just easier to run it here rather than in a 
# separate function

Safari = app(u'/Applications/Safari.app')
url = Safari.documents[0].URL()
FEdoc = Safari.documents[0].get()

# list of urls that require custom code and uses either the  ID or class of their search field
custom_urls = [
        ["arstechnica.com/civis","keywords"],
        ]

def focuswidget(url):
    for c in custom_urls:
        if c[0] in url:
        
            Safari.do_JavaScript(s_id.format(c[1]), in_=FEdoc)
            return
    Safari.do_JavaScript(javascript, in_=FEdoc)
    return
    
    
def injectjava():
    Safari.activate()
    focuswidget(url)

    # select all within the text widget
    app(u'System Events').keystroke(u'a', using=k.command_down)
    return
    
if __name__ == '__main__':
    injectjava()
