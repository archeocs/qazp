# -*- coding: utf-8 -*-

# dane typu slownikowego

class Slow:
    
    MIASTA, POWIATY, WOJEWODZ, GMINY, KULTURY,FUNKCJE,EPOKI = 1,2,3,4,5,6,7
    var_slo = {MIASTA:('miasta_slo','miejscowosc'),
               POWIATY:('powiaty_slo','powiat'),
               WOJEWODZ:('wojewodztwa_slo','wojewodztwo'),
               GMINY:('gminy_slo','gmina'),
               KULTURY:('kultury_slo','kultura'),
               FUNKCJE:('funkcje_slo','funkcja'),
               EPOKI:('epoki_slo','epoka')}
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
        return self.var_slo[self.t]
            
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
        if self.slow.has_key(nv.upper()):
            return (False,u'Nazwa już istnieje')
        if self.zmiany.has_key(k) and self.zmiany[k].czy_new:
            e.n = nv.upper()
            e.czy_new = True
            self.slow.pop(k)
            self.zmiany.pop(k)
            self.slow[e.n] = e
            self.zmiany[e.n] = e
            return (True,'')
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
            return (True,'')
        else:
            return (False,u'Nazwa przeznaczona do usunięcia') # wskazany element zostal juz usuniety
            
    def lista(self,nowa=False):
        #tb = self.slow.values()
        #tb.sort()
        if nowa:
            self.tb = self.slow.values()
            self.tb.sort()
        return self.tb
        
    def zapisz(self):
        #ins = "select * from azp_%s('%s')"
        ins = "insert into %s values(%d,'%s')"
        updt = "update %s set nazwa = '%s' where sid = %s"
        delit = "delete from %s where sid=%s"

        for e in self.zmiany.values():
            if e.czy_new:
                sql = ins%(self.var_slo[self.t][0],self.max_sid(self.var_slo[self.t][0]),e.n)
                self.con.wykonaj(sql,False)
                #return (True,'')
            elif e.czy_mod:
                self.con.wykonaj(updt%(self.var_slo[self.t][0],e.n,str(e.i)),False)
                #return (True,'')
            elif e.czy_del:
                self.con.wykonaj(delit%(self.var_slo[self.t][0],str(e.i)),False)
                #return (True,'')
        self.con.zatwierdz()
        return (True,'')
    
    def spr_usun(self,klucz):
        e = self.slow[klucz]
        if e.czy_new:
            return (True,'')
        if self.t < self.KULTURY and self.spr_czy_lok(e,self.var_slo[self.t][1]):
            return (False,u'Usuwana nazwa została już użyta')
        elif self.t > self.GMINY and self.spr_czy_fakt(e, self.var_slo[self.t][1]):
            return (False,u'Usuwana nazwa została już użyta')
        else:
            return (True,'')
    
    def spr_czy_lok(self,e,pn):
        sql = "select count(*) from lokalizacje where %s = %d" %(pn,e.i)
        print sql
        ile = self.con.wykonaj(sql)
        return ile[0][0] > 0 # istnieje lokalizacja do ktorej przypisana jest uswana nazwa 
    
    def spr_czy_fakt(self,e,pn):
        sql = "select count(*) from materialy where %s = %d" %(pn,e.i)
        ile = self.con.wykonaj(sql)
        return ile[0][0] > 0 # istnieje lokalizacja do ktorej przypisana jest uswana nazwa     
        
    def max_sid(self,tab):
        max_id = "select coalesce(max(sid),0)+1 as nast from %s" % tab
        mt = self.con.wykonaj(max_id)
        return mt[0][0]    
        
    def nazwa_sid(self,n):
        if isinstance(n,unicode):
            return self.slow[n].i
        else:
            return self.slow[n.decode('utf-8')].i
            
    def indeks_sid(self,i):
        if i >= 0:
            return self.nazwa_sid(self.tb[i])
        return -1
    
    #def sid_indeks(self,sid):    
        
    def nazwa_ind(self,n):
        if n is None:
            return -1
        if isinstance (n,unicode):
            return self.slow[n].ti
        else:
            return self.slow[n.decode('utf-8')].ti
    
    def indeks_naz(self,ind):
        return self.tb[ind]
            
            
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
    
    def __unicode__(self):
        return self.n