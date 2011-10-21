'''
Created on Oct 15, 2011

@author: milosz
'''

class Zagrozenie(object):
    czy_zm = False
    nowe = False
    modstr = "select * from azp_zmien_zagrozenie(%d,'%s','%s','%s','%s','%s','%s','%s', %d)"
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 8:
            zm = {'T':1,'N':0}
            self.istn, self.stal, self.ludz, self.nat = zm[td[1]],zm[td[2]],zm[td[3]],zm[td[4]]
            self.pryw,self.spol = zm[td[5]],zm[td[6]]
            self.dodat = td[7].decode('utf-8')
            self.zid = td[0]
        else:
            self.istn, self.stal, self.doraz, self.ludz, self.nat = 0,0,0,0,0
            self.pryw,self.spol = 0,0
            self.dodat = u''
            self.zid = -1
            self.nowe = True
        self.p = con
        self.stan = stan

    def zmien(self,var,val):
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_zm = True
        
    def zapisz(self):
        print 'zapisuje'
        if self.czy_zm:
            zm = {1:'T',0:'N'}
            args = (self.stan.sid,zm[self.istn],zm[self.stal],zm[self.ludz],zm[self.nat],
                    zm[self.pryw],zm[self.spol],self.dodat,self.zid)
            print self.modstr % args
            self.p.wykonaj(self.modstr % args)
            self.p.zatwierdz()
        else:
            print 'ZAGROZENIE: brak zmian'
        