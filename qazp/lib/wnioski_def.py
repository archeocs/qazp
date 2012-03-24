'''
Created on Oct 1, 2011

@author: milosz
'''

class Wnioski:
    czy_nowy=True
    czy_mod = False
    modstr = "select * from azp_zmien_wniosek(%d, %d, '%s', '%s', '%s', '%s', %d)"
    def __init__(self,stan,con,tab_dane=None):
        if tab_dane is not None and len(tab_dane) == 7:
            zm = {'T':1,'N':0}
            self.wartosc, self.inwent, self.interw, self.wykopy = tab_dane[2], zm[tab_dane[3]], zm[tab_dane[4]], zm[tab_dane[5]]
            self.dodat = tab_dane[6].decode('utf-8')
            self.wid = tab_dane[0]
        else:
            self.wartosc, self.inwent, self.interw,self.wykopy = 0,0,0,0
            self.dodat = ""
            self.wid = -1
            self.nowe = True
        self.p = con
        self.stan = stan
        
    def zmien(self,var,val):
        print var, val, hasattr(self,var), getattr(self,var,None)
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_mod = True
            
    def max_wid(self):
        max_id = "select coalesce(max(wid),0)+1 as nast from wnioski"
        mt = self.p.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        #(nast,stanowisko,obser,obpole,nasyc,gest,powierz,centrycz)
        ins = """ insert into wnioski values(%(wid)s,%(sid)s,%(wart)s,'%(inwent)s','%(interw)s','%(wykopy)s','%(dodat)s')"""
        updt = """update wnioski set wart_pozn = %(wart)s, inwentaryzacja = '%(inwent)s', interwencja = '%(interw)s',
         wykopaliska = '%(wykopy)s',dodatkowe = '%(dodat)s' where wid = %(wid)s"""            
        if self.wid < 0:
            mw = self.max_wid() 
            sqlargs['wid'] = str(mw)
            sql = ins % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        else:
            sql = updt % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        self.p.zatwierdz()
    
    
        
    def zapisz(self):
        if self.czy_mod:
            zm = {1:'T',0:'N'}
            sqlargs = {'sid':str(self.stan.sid),'wart':str(self.wartosc),'inwent':zm[self.inwent],'interw':zm[self.interw],
                       'wykopy':zm[self.wykopy],'dodat':self.dodat,'wid':str(self.wid)}
            self.moddb(sqlargs)
        else:
            print 'WNIOSKI brak zmian'
        