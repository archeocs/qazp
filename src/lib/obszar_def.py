'''
Created on Jul 23, 2011

@author: milosz
'''

class Obszar(object):
    #obserwacja,orne,nasycenie,gestosc, powierzchnia, centrycznosc, oid
    czy_nowy=True
    czy_mod = False
    modstr = "select * from azp_zmien_obszar(%d,%d,%d,%d,%d,%d,%d,%d)"
    def __init__(self,stan,con,dbinfo=None):
        if dbinfo is None:
            self.obser,self.pole,self.nasyc = 0,0,0
            self.gest, self.powierz, self.idobsz = 0,0,-1
            self.centr = 0
            self.stan = stan
            self.con = con
        else:
            self.obser,self.pole,self.nasyc = dbinfo[0],dbinfo[1],dbinfo[2]
            self.gest,self.powierz,self.idobsz = dbinfo[3],dbinfo[4],dbinfo[5]
            self.centr = dbinfo[6]
            self.czy_nowy = False
        self.stan = stan
        self.con = con

    def zmien(self,var,val):
        print var,val
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_mod = True
    
    def zapisz(self):
        if self.czy_mod:
            args = (self.stan.sid,self.obser,self.pole,self.nasyc,self.gest,self.powierz,self.centr,self.idobsz) 
            self.con.wykonaj(self.modstr % args)
            self.con.zatwierdz()
            print self.modstr % args
        else:
            print 'Obszar: brak zmian'   