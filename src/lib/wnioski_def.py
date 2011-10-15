'''
Created on Oct 1, 2011

@author: milosz
'''

class Wnioski:
    czy_nowy=True
    czy_mod = False
    modstr = "select * from azp_zmien_wniosek(%d, %d, '%s', '%s', '%s', '%s', %d)"
    def __init__(self,stan,con,tab_dane=None):
        if tab_dane is not None and len(tab_dane) == 7:
            zm = {'T':1,'N':0}
            self.wartosc, self.inwent, self.interw, self.wykopy = tab_dane[2], zm[tab_dane[3]], zm[tab_dane[4]], zm[tab_dane[5]]
            self.dodat = tab_dane[6].decode('utf-8')
            self.wid = tab_dane[0]
        else:
            self.wartosc, self.inwent, self.interw,self.wykopy = 0,0,0,0
            self.dodat = ""
            self.wid = -1
            self.nowe = True
        self.p = con
        self.stan = stan
        
    def zmien(self,var,val):
        print var, val, hasattr(self,var), getattr(self,var,None)
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_mod = True
        
    def zapisz(self):
        if self.czy_mod:
            zm = {1:'T',0:'N'}
            print self.modstr % (self.stan.sid,self.wartosc,zm[self.inwent],zm[self.interw],zm[self.wykopy],self.dodat,self.wid)
            self.p.wykonaj(self.modstr % (self.stan.sid,self.wartosc,zm[self.inwent],zm[self.interw],zm[self.wykopy],self.dodat,self.wid))
            self.p.zatwierdz()
        else:
            print 'WNIOSKI brak zmian'
        