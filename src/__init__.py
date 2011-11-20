'''
Created on Jul 29, 2011

@author: milosz
'''

def name():
    return "QAZP"

def description():
    return "Archeologiczne Zdjecie Polski"

def version():
    return "Version 0.99"

def qgisMinimumVersion():
    return "1.5"

def authorName():
    return "Milosz Piglas"

def classFactory(iface):
    import qazp
    return qazp.QGisPlugin(iface)