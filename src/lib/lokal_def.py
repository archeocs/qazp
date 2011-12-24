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
    
    def max_lid(self):
        max_id = "select coalesce(max(lid),0)+1 as nast from lokalizacje"
        mt = self.con.wykonaj(max_id)
        return mt[0][0]
        
    def moddb(self,sqlargs):
        ins = """ insert into lokalizacje values(%(lid)s,'%(ark)s','%(nr_ark)s', %(miej_id)s, '%(nr_miej)s', %(gm)s, %(pow)s, %(woj)s)"""
        stan_nowa_lok = """update stanowiska set arkusz = '%(ark)s', nr_arkusz = '%(nr_ark)s', lokalizacja = %(lid)s,
                             miejscowosc = '%(naz_miej)s', nr_miejscowosc='%(nr_miej)s' where sid = %(sid)s """
        stan_mod_lok = """ update stanowiska set arkusz = '%(ark)s', nr_arkusz = '%(nr_ark)s', miejscowosc = '%(naz_miej)s',
                                 nr_miejscowosc='%(nr_miej)s' where lokalizacja = %(lid)s """
        updt_lok = """update lokalizacje set arkusz = '%(ark)s', nr_arkusz = '%(nr_ark)s', miejscowosc = %(miej_id)s, 
                            nr_miejscowosc = '%(nr_miej)s', gmina =%(gm)s, powiat =%(pow)s, wojewodztwo =%(woj)s where lid = %(lid)s """
        if self.gm_id == -1:
            sqlargs['gm'] = 'null'
        if self.pow_id == -1:
            sqlargs['pow'] = 'null'
        if self.woj_id == -1:
            sqlargs['woj'] = 'null'            
        if self.czy_nowa:
            ml = self.max_lid() 
            sqlargs['lid'] = str(ml)
            sql = ins % sqlargs
            print sql
            self.con.wykonaj(sql,False)
            sql = stan_nowa_lok % sqlargs
            print sql
            self.con.wykonaj(sql,False)
        elif self.czy_zm:
            print sqlargs
            sql = updt_lok % sqlargs
            print sql
            self.con.wykonaj(sql,False)
            sql = stan_mod_lok % sqlargs
            print sql
            self.con.wykonaj(sql,False)
            #self.con.wykonaj(sql,False)
        self.con.zatwierdz()
                
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
        print 'czy nowa',self.czy_nowa
        sqlargs = {'lid':str(self.stan.lokalizacja), 'ark':self.arkusz, 'nr_ark':self.nr_ark, 'miej_id':str(self.miej_id), 
                   'nr_miej':self.nr_miej, 'gm':str(self.gm_id), 'pow':str(self.pow_id), 'woj':str(self.woj_id),
                   'naz_miej':self.miej_naz,'sid':self.stan.sid}
        #if self.czy_nowa:
        #    self.dodaj()
        #else:
        #    self.zmien()
        self.moddb(sqlargs)
            
    def __str__(self):
        print "LOKALIZACJA INFO"
        print self.arkusz
        print self.nr_ark
        print self.miej_naz
        print self.gm_naz
        print self.pow_naz
        print self.woj_naz
        return self.arkusz+"/"+self.nr_ark