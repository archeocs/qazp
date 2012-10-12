'''
Created on Sep 9, 2012

@author: milosz
'''

import sys
sys.path.extend(__path__)

def name():
    return "TEST QAZP2"

def description():
    return "test qazp2"

def version():
    return "Version 0.3"

def qgisMinimumVersion():
    return "1.6"

def authorName():
    return u"Milosz Piglas"

def classFactory(iface):
    import qazp
    return qazp.QazpPlugin(iface)
