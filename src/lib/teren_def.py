'''
Created on Jul 8, 2011

@author: milosz
'''
# informacja o terenie

class Teren:
    # tab_dane = [tid,sid,pole_orne,sad,torf,nieuzytek,park,laka,bagno,las,zabud,niezabud,srednio_zabud, okresl bliz
    nowe = False
    czy_zm = False
    modstr = "select * from azp_zmien_teren(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d)"
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 14:
            zm = {'T':1,'N':0}
            self.tid = td[0]
            self.orne,self.sad,self.pryw,self.spol,self.park,self.laka = zm[td[2]],zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]]
            self.przem,self.las,self.zab,self.niezab,self.srezab = zm[td[8]],zm[td[9]],zm[td[10]],zm[td[11]],zm[td[12]]
            self.bliz = td[13].decode('utf-8')
            #self.tid = td[0]
        else:
            self.orne,self.sad,self.pryw,self.spol,self.park,self.laka = 0,0,0,0,0,0
            self.przem,self.las,self.zab,self.niezab,self.srezab = 0,0,0,0,0,
            self.bliz = ""
            self.tid = -1
            self.nowe = True
        self.p = con
        self.stan = stan
    
    def zmien(self,var,val):
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_zm = True
    
    def zapisz(self):
        if self.czy_zm:
            zm = {1:'T',0:'N'}
            args = (self.stan.sid,zm[self.orne],zm[self.sad],zm[self.pryw],zm[self.spol],zm[self.park],
                    zm[self.laka],zm[self.przem],zm[self.las],zm[self.zab],zm[self.niezab],zm[self.srezab],
                    self.bliz,self.tid)
            print self.modstr % args
            self.p.wykonaj(self.modstr % args)
            self.p.zatwierdz()
        else:
            print "TEREN: brak zmian"