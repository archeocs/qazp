# -*- coding: utf-8 -*-

'''
Created on Mar 23, 2012

@author: milosz
'''

def name():
    return "GPS-Azp"

def description():
    return u"Import danych GPS do przestrzennej bazy danych"

def version():
    return "Version 0.1"

def qgisMinimumVersion():
    return "1.6"

def authorName():
    return u"Miłosz Pigłas"

def classFactory(iface):
    import plugin
    return plugin.Plugin(iface)