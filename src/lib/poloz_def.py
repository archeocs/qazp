'''
Created on Jul 8, 2011

@author: milosz
'''
# informacja o polozeniu okreslonym w momencie wejscia. Odnosi sie do okreslonego stanowiska

class Polozenie:
    czy_zm = False
    nowe = False
    modstr = "select * from azp_zmien_polozenie(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', %d)"
    #pid stanowisko jednostka morze  plaza  mierzeja  skarpa  wal_wydma woda  terasa_denna  terasa_nadzalew 
    # terasa_wyzsza dno_doliny  stok_doliny kraw_doliny rownina  obsz_falisty obsz_pagor  obszar_gorz
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 19:
            zm = {'T':1,'N':0}
            self.jedn = td[2].decode('utf-8')
            self.morze,self.plaza,self.mierz,self.skarpa,self.wal,self.woda,self.terden = zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]],zm[td[8]],zm[td[9]]
            self.ternad,self.terwyz,self.dnod,self.stokd,self.krawd,self.rown,self.fal = zm[td[10]],zm[td[11]],zm[td[12]],zm[td[13]],zm[td[14]],zm[td[15]],zm[td[16]]
            self.pagor,self.gorz = zm[td[17]],zm[td[18]]
            self.pid = td[0]
        else:
            self.jedn = u""
            self.morze,self.plaza,self.mierz,self.skarpa,self.wal,self.woda,self.terden = 0,0,0,0,0,0,0
            self.ternad,self.terwyz,self.dnod,self.stokd,self.krawd,self.rown,self.fal = 0,0,0,0,0,0,0
            self.pagor,self.gorz = 0,0
            self.pid = -1
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
            args = (self.stan.sid,self.jedn, zm[self.morze], zm[self.plaza], zm[self.mierz], zm[self.skarpa], zm[self.wal], zm[self.woda], zm[self.terden], zm[self.ternad], zm[self.terwyz],zm[self.dnod],zm[self.stokd],zm[self.krawd],zm[self.rown],zm[self.fal],zm[self.pagor],zm[self.gorz], self.pid)
            self.p.wykonaj(self.modstr % args)
            self.p.zatwierdz()
        else:
            print 'POLOZENIE: brak zmian'