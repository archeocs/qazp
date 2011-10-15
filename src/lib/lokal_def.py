'''
Created on Jul 8, 2011

@author: milosz
'''
# reprezentuje pojedyncza lokalizacje AZP reprezentowana przez arkusz i nr na arkuszu

class Lokalizacja:
    
    miej_id, gm_id, pow_id, woj_id = -1,-1,-1,-1
    arkusz,nr_ark,nr_miej,miej_naz,gm_naz,pow_naz,woj_naz = None,None,u"",None,None,None,None
    czy_nowa = False
    czy_zm = False
    instr = "select * from azp_nowa_lokalizacja('%s','%s',%d,'%s',%d,%d,%d,%d)"
    # instr ark, nr_ark, miej, nr_miej, gmina, powiat,wojew,do_stan [przy ktorym stan byla utworzona
    updtstr = "select * from azp_zmien_lokalizacja(%d,'%s','%s',%d,'%s',%d,%d,%d,%d)"
    # updtstr lokalizacja,ark, nr_ark, miej, nr_miej, gmina, powiat,wojew,czy_akt [czy zmienic wszystkie stanowiska do ktorych jest przypisana lokalizacja]
    
    def __init__(self,stan,con,tab_dane=None):
        if tab_dane is None:
            self.czy_nowa = True
            self.arkusz = stan.arkusz
            self.nr_ark = stan.nr_ark
        else:
            self.arkusz = tab_dane[0].decode('utf-8')
            self.nr_ark = tab_dane[1].decode('utf-8')
            self.miej_naz = tab_dane[2].decode('utf-8')
            self.miej_id = tab_dane[3]
            self.nr_miej = tab_dane[4].decode('utf-8')
            self.gm_naz = tab_dane[5].decode('utf-8')
            self.gm_id = tab_dane[6]
            if tab_dane[7] is not None:
                self.pow_naz = tab_dane[7].decode('utf-8')
                self.pow_id = tab_dane[8]
            if tab_dane[9] is not None:
                self.woj_naz = tab_dane[9].decode('utf-8')
                self.woj_id = tab_dane[10]
        self.stan = stan
        self.con = con
                
    def zmien(self):
        akt = -1
        if self.czy_zm:
            akt = 1
        s = self.updtstr % (self.stan.lokalizacja,self.arkusz,self.nr_ark,self.miej_id,self.nr_miej,self.gm_id,
                              self.pow_id,self.woj_id,akt)
        print 'funkcja '+s
        self.con.wykonaj(s)
        self.con.zatwierdz()
        
    def dodaj(self):
        print self.instr % (self.arkusz,self.nr_ark,self.miej_id,self.nr_miej,self.gm_id,self.pow_id,self.woj_id,self.stan.sid)
        self.con.wykonaj(self.instr % (self.arkusz,self.nr_ark,self.miej_id,self.nr_miej,self.gm_id,self.pow_id,self.woj_id,self.stan.sid))
        self.con.zatwierdz()
                
    def zapisz(self):
        print self.czy_nowa
        if self.czy_nowa:
            self.dodaj()
        else:
            self.zmien()
            
    def __str__(self):
        print "LOKALIZACJA INFO"
        print self.arkusz
        print self.nr_ark
        print self.miej_naz
        print self.gm_naz
        print self.pow_naz
        print self.woj_naz
        return self.arkusz+"/"+self.nr_ark