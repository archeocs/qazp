'''
Created on Jul 8, 2011

@author: milosz
'''
# informacja o ekspozycji stanowiska
class Ekspozycja:
    # tab_dane = [eksponowany,kraw_stok,sfal_cypel,cypl,wal_garb,okrezna,podst_stoku,dolina_niecka,kotl_zagl,jaskinia,eid]
    czy_zm = False
    nowe = False
    modstr = """select * from azp_zmien_ekspozycje(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
                    '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d)"""
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 22:
            zm = {'T':1,'N':0}
            self.czy_eksp,self.kraw,self.sfal,self.cypel,self.wal,self.okrez = zm[td[2]],zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]]
            self.oslo,self.stok, self.dolina,self.kotl,self.jask = zm[td[8]],zm[td[9]],zm[td[10]],zm[td[11]],zm[td[12]]
            self.szczegolna = td[13].decode('utf-8')
            self.n,self.ne,self.e,self.se,self.s,self.sw = zm[td[14]],zm[td[15]],zm[td[16]],zm[td[17]],zm[td[18]],zm[td[19]]
            self.w,self.nw =  zm[td[20]],zm[td[21]]
            self.eid = td[0]
        else:
            self.kraw, self.czy_eksp, self.sfal, self.cypel, self.wal, self.okrez = 0,0,0,0,0,0
            self.oslo, self.stok, self.dolina, self.kotl, self.jask, self.eid = 0,0,0,0,0,-1
            self.szczegolna = ''
            self.n,self.ne,self.e,self.se,self.s,self.sw = 0,0,0,0,0,0
            self.w,self.nw =  0,0
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
            self.p.wykonaj(self.modstr % (self.stan.sid,zm[self.czy_eksp],zm[self.kraw],zm[self.sfal],zm[self.cypel],
                                          zm[self.wal],zm[self.okrez],zm[self.oslo],zm[self.stok],zm[self.dolina],zm[self.kotl],
                                          zm[self.jask],self.szczegolna,zm[self.n],zm[self.ne],zm[self.e],zm[self.se],
                                          zm[self.s],zm[self.sw],zm[self.w],zm[self.nw],self.eid))
            self.p.zatwierdz()
        else:
            print 'EKSPOZYCJA brak zmian'