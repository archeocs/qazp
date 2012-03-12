# -*- coding: utf-8 -*-

'''
Created on Jul 29, 2011

@author: milosz
'''

def name():
    return "QAZP"

def description():
    return u"Archeologiczne Zdjęcie Polski"

def version():
    return "Version 0.13"

def qgisMinimumVersion():
    return "1.6"

def authorName():
    return "Miłosz Pigłas"

def classFactory(iface):
    import qazp
    return qazp.QGisPlugin(iface)