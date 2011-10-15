# -*- coding: utf-8 -*-

# dane typu slownikowego

class Slow:
    
    MIASTA, POWIATY, WOJEWODZ, GMINY, KULTURY,FUNKCJE,EPOKI = 1,2,3,4,5,6,7
    def __init__(self,lista,con,typ):
        self.slow = {}
        self.zmiany = {}
        self.con = con
        self.t = typ
        self.tb = []
        for (ei,e) in enumerate(lista):
            n = e[1].decode('utf-8')
            self.slow[n] = E(n,e[0],ei)
            self.tb.append(n)
            
    def nazwa(self):
        if self.t == self.MIASTA:
            return u'Miasta'
        elif self.t == self.POWIATY:
            return u'Powiaty'
        elif self.t == self.WOJEWODZ:
            return u'Województwa'
        elif self.t == self.GMINY:
            return u'Gminy'
        elif self.t == self.KULTURY:
            return u'Kultury'
        elif self.t == self.FUNKCJE:
            return u'Funkcje'
        elif self.t == self.EPOKI:
            return u'Epoki'
            
    def nowy(self,nv):
        unv = nv.upper()
        if not self.slow.has_key(unv):
            e = E(unv,-1)
            e.czy_new = True
            self.slow[e.n] = e
            self.zmiany[e.n] = e
            return (e,True)
        else:
            return (None,False)
            
    def usun(self,k):
        e = self.slow[k]
        if self.zmiany.has_key(k) and self.zmiany[k].czy_new:
            self.slow.pop(k)
            self.zmiany.pop(k)
            return True
        elif not self.zmiany.has_key(k) or self.zmian[k].czy_mod:
            e.czy_mod = False
            e.czy_new = False
            e.czy_del = True
            self.slow.pop(k)
            self.zmiany[k] = e
            return True
        else:
            return False
    
    def zmien(self,k,nv):
        e = self.slow[k]
        if self.zmiany.has_key(k) and self.zmiany[k].czy_new:
            e.n = nv.upper()
            e.czy_new = True
            self.slow.pop(k)
            self.zmiany.pop(k)
            self.slow[e.n] = e
            self.zmiany[e.n] = e
            return True
        elif not self.zmiany.has_key(k) or not self.zmiany[k].czy_del:
            e.n = nv.upper()
            e.czy_mod = True
            self.slow.pop(k)
            #self.zmiany.pop(k)
            #self.slow[k] = e
            if self.zmiany.has_key(k):
                self.zmiany.pop(k)
                self.zmiany[k] = e
            self.slow[e.n] = e
            self.zmiany[e.n] = e
            return True
        else:
            return False # wskazany element zostal juz usuniety
            
    def lista(self,nowa=False):
        #tb = self.slow.values()
        #tb.sort()
        if nowa:
            self.tb = self.slow.values()
            self.tb.sort()
        return self.tb
        
    def zapisz(self):
        ins = "select * from azp_%s('%s')"
        updt = "update %s set nazwa = '%s' where sid = %s"
        if self.t == self.MIASTA:
            naz_u = 'miasta_slo'
            naz_i = 'nowe_miasto'
        elif self.t == self.POWIATY:
            naz_u = 'powiaty_slo'
            naz_i = 'nowy_powiat'
        elif self.t == self.WOJEWODZ:
            naz_u = 'wojewodztwa_slo'
            naz_i = 'nowe_wojewodztwo'
        elif self.t == self.GMINY:
            naz_u = 'gminy_slo'
            naz_i = 'nowa_gmina'
        elif self.t == self.KULTURY:
            naz_u = 'kultury_slo'
            naz_i = 'nowa_kultura'
        elif self.t == self.FUNKCJE:
            naz_u = 'funkcje_slo'
            naz_i = 'nowa_funkcja'
        elif self.t == self.EPOKI:
            naz_u = 'epoki_slo'
            naz_i = 'nowa_epoka'
        for e in self.zmiany.values():
            if e.czy_new:
                self.con.wykonaj(ins%(naz_i,e.n))
            elif e.czy_mod:
                self.con.wykonaj(updt%(naz_u,e.n,str(e.i)),False)
        self.con.zatwierdz()
        
    def nazwa_sid(self,n):
        if isinstance(n,unicode):
            return self.slow[n].i
        else:
            return self.slow[n.decode('utf-8')].i
            
    def indeks_sid(self,i):
        if i >= 0:
            return self.nazwa_sid(self.tb[i])
        return -1
        
    def nazwa_ind(self,n):
        if n is None:
            return -1
        if isinstance (n,unicode):
            return self.slow[n].ti
        else:
            return self.slow[n.decode('utf-8')].ti
            
            
class E:
    
    czy_mod = False
    czy_del = False
    czy_new = False
    def __init__(self,nazwa,sid,tab_ind=-1):
        if isinstance(nazwa,unicode):
            self.n = nazwa
        else:
            self.n = nazwa.decode('utf-8')
        self.i = sid
        self.ti = tab_ind
        
    #def __unicode__(self):
    #    return unicode(uzytki.to_unicode(self.n))
    
    def __unicode__(self):
        return self.n