'''
Created on Jul 23, 2011

@author: milosz
'''

class Obszar(object):
    #obserwacja,orne,nasycenie,gestosc, powierzchnia, centrycznosc, oid
    czy_nowy=True
    czy_mod = False
    #modstr = "select * from azp_zmien_obszar(%d,%d,%d,%d,%d,%d,%d,%d)"
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
    
    def max_oid(self):
        max_id = "select coalesce(max(oid),0)+1 as nast from obszary"
        mt = self.con.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        #(nast,stanowisko,obser,obpole,nasyc,gest,powierz,centrycz)
        ins = """ insert into obszary values(%(oid)s,%(sid)s,%(obser)s,%(pole)s,%(nasyc)s,
                                                %(gest)s,%(powierz)s,%(centr)s)"""
        #update obszary set obserwacja = obser, pole = obpole, nasycenie = nasyc, gestosc = gest,
        #powierzchnia = powierz, centrycznosc = centrycz where oid = obsz_id;
        updt = """update obszary set obserwacja = %(obser)s, pole = %(pole)s,nasycenie =%(nasyc)s, gestosc =%(gest)s,
            powierzchnia = %(powierz)s, centrycznosc =%(centr)s where oid =%(oid)s;"""            
        if self.idobsz < 0:
            mo = self.max_oid() 
            sqlargs['oid'] = str(mo)
            sql = ins % sqlargs
            print sql
            self.con.wykonaj(sql,False)
        else:
            sql = updt % sqlargs
            print sql
            self.con.wykonaj(sql,False)
        self.con.zatwierdz()
    
    
    def zapisz(self):
        if self.czy_mod:
            #args = (self.stan.sid,self.obser,self.pole,self.nasyc,self.gest,self.powierz,self.centr,self.idobsz) 
            #self.con.wykonaj(self.modstr % args)
            #self.con.zatwierdz()
            #print self.modstr % args
            sqlargs = {'oid':str(self.idobsz),'sid':str(self.stan.sid),'obser':str(self.obser),'pole':str(self.pole), 
                       'nasyc':str(self.nasyc), 'gest':str(self.gest),'powierz':str(self.powierz),'centr':str(self.centr)}
            self.moddb(sqlargs)
        else:
            print 'Obszar: brak zmian'   