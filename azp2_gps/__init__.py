# -*- coding: utf-8 -*-

'''
Licencja BSD
Milosz Piglas
'''

def name():
    return "AZP2-GPS"

def description():
    return u"Import danych GPS do przestrzennej bazy danych"

def version():
    return "Version 0.2"

def qgisMinimumVersion():
    return "1.6"

def authorName():
    return u"Miłosz Pigłas"

def classFactory(iface):
    import plugin
    return plugin.Plugin(iface)
