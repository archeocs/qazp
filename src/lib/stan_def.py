'''
Created on Jul 8, 2011

@author: milosz
'''
# reprezentuje wejscie na stanowisko

class Stanowisko:
    
    sid = -1
    rodzaj = None
    arkusz = None
    nr_ark = None
    miejsce = None
    nr_miejsce = None
    autor = None
    data = None
    wspolrzedne = None
    lokalizacja = None
    
    def __init__(self,tup):
        self.sid = tup[0]
        self.rodzaj = tup[1].decode('utf-8')
        self.arkusz = tup[2].decode('utf-8')
        self.nr_ark = tup[3].decode('utf-8')
        self.miejsce = tup[4].decode('utf-8')
        self.nr_miejsce = tup[5].decode('utf-8')
        self.wspolrzedne = tup[6].decode('utf-8')
        self.data = tup[7]
        self.autor = tup[8].decode('utf-8')
        self.lokalizacja = tup[9]
        
    def __str__(self):
        return '%s / %s (%s)' % (self.arkusz,self.nr_ark,self.data)

