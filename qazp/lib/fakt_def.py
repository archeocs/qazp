'''
Created on Jul 8, 2011

@author: milosz
'''
class Fakt:
    epoka,kultura,funkcja,cer,kam,met = 0,0,0,0,0,0
    epoka_nazwa, kultura_nazwa,funkcja_nazwa = "","",""
    mas,  wyod = "", ""
    mid = -1
    czy_nowy = True
    czy_mod = False
    #modstr = "select * from azp_zmien_materialy(%d,%d,%d,%d,%d,%d,'%s','%s',%d,%d)" # epoka,kultura,funkcja,cer,kam,met,stan.sid,mid
    def __init__(self,stan,con,tf=[]):
        self.stan = stan
        self.con = con    
        if len(tf) == 12:
            self.epoka = tf[1]
            self.kultura = tf[2]
            self.funkcja = tf[3]
            self.cer = tf[4]
            self.kam = tf[5]
            self.met = tf[6]
            self.mid = tf[0]
            self.epoka_nazwa = tf[7].decode('utf-8')
            self.kultura_nazwa = tf[8].decode('utf-8')
            self.funkcja_nazwa = tf[9].decode('utf-8')
            self.mas = tf[10].decode('utf-8')
            self.wyod = tf[11].decode('utf-8')
            self.czy_nowy = False
            print tf
     
    def set_wartosc(self,zm,wart):
        if hasattr(self, zm) and wart != getattr(self, zm):
            self.czy_mod = True
            setattr(self, zm, wart)
            return True
        return False
    
    def set_epoka(self,ident,naz):
        if self.set_wartosc("epoka",ident):
            return self.set_wartosc("epoka_nazwa", naz)
        return False
            
    def set_kultura(self,ident,naz):
        if self.set_wartosc("kultura",ident):
            return self.set_wartosc("kultura_nazwa", naz)
        return False
    
    def set_funkcja(self,ident,naz):
        if self.set_wartosc("funkcja",ident):
            return self.set_wartosc("funkcja_nazwa", naz)
        return False        
    
    def max_eid(self):
        max_id = "select coalesce(max(mid),0)+1 as nast from materialy"
        mt = self.con.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        ins = """ insert into materialy values(%(mid)s,%(sid)s,%(ep)s,%(kul)s,%(fun)s,%(cer)s,
                        %(kam)s,%(met)s,'%(mas)s','%(wyod)s')"""
        
        updt = """update materialy set epoka=%(ep)s,kultura=%(kul)s,funkcja=%(fun)s,
                ceramika=%(cer)s,kamien=%(kam)s,metal=%(met)s,masowy='%(mas)s',wyodrebniony='%(wyod)s'
                where mid=%(mid)s """
        if self.epoka == 0:
            sqlargs['ep'] = 'null'
        if self.kultura == 0:
            sqlargs['kul'] = 'null'
        if self.funkcja == 0:
            sqlargs['fun'] = 'null'            
        if self.mid < 0:
            mm = self.max_eid() 
            sqlargs['mid'] = str(mm)
            sql = ins % sqlargs
            print sql
            self.con.wykonaj(sql,False)
        else:
            print sqlargs
            sql = updt % sqlargs
            print sql
            self.con.wykonaj(sql,False)
        self.con.zatwierdz()        
            
    def zapisz(self):
        if self.czy_mod:
            sqlargs = {'mid':str(self.mid),'sid':str(self.stan.sid),'ep':str(self.epoka),'kul':str(self.kultura),
                       'fun':str(self.funkcja),'cer':str(self.cer),'kam':str(self.kam),'met':str(self.met),
                       'mas':self.mas,'wyod':self.wyod}
            self.moddb(sqlargs)
            #sql = self.modstr % (self.epoka,self.kultura,self.funkcja,self.cer,self.kam,self.met,self.mas, self.wyod, self.stan.sid,self.mid)
            #self.con.wykonaj(sql)
            #self.con.zatwierdz()
            
    def __unicode__(self):
        return 'epoka: %d\nkultura: %d\n:funkcja: %d\n %d %d %d %s %s %s' % (self.epoka,self.kultura,self.funkcja,self.cer,self.kam,self.met,self.epoka_nazwa,self.kultura_nazwa,self.funkcja_nazwa)