'''
Created on Oct 15, 2011

@author: milosz
'''

class Zagrozenie(object):
    czy_zm = False
    nowe = False
    modstr = "select * from azp_zmien_zagrozenie(%d,'%s','%s','%s','%s','%s','%s','%s', %d)"
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 8:
            zm = {'T':1,'N':0}
            self.istn, self.stal, self.ludz, self.nat = zm[td[1]],zm[td[2]],zm[td[3]],zm[td[4]]
            self.pryw,self.spol = zm[td[5]],zm[td[6]]
            self.dodat = td[7].decode('utf-8')
            self.zid = td[0]
        else:
            self.istn, self.stal, self.doraz, self.ludz, self.nat = 0,0,0,0,0
            self.pryw,self.spol = 0,0
            self.dodat = u''
            self.zid = -1
            self.nowe = True
        self.p = con
        self.stan = stan

    def zmien(self,var,val):
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_zm = True
    
    def max_zid(self):
        max_id = "select coalesce(max(zid),0)+1 as nast from zagrozenia"
        mt = self.p.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        #(nast,stanowisko,obser,obpole,nasyc,gest,powierz,centrycz)
        ins = """ insert into zagrozenia values(%(zid)s,%(sid)s,'%(istn)s','%(stal)s','%(ludz)s','%(natu)s',
                '%(pryw)s','%(spol)s','%(dodat)s')"""
        #update obszary set obserwacja = obser, pole = obpole, nasycenie = nasyc, gestosc = gest,
        #powierzchnia = powierz, centrycznosc = centrycz where oid = obsz_id;
        updt = """update zagrozenia set istnieje = '%(istn)s', stale = '%(stal)s', ludzie='%(ludz)s', natura='%(natu)s',
        prywatny='%(pryw)s', spoleczny='%(spol)s', dodatkowe = '%(dodat)s' where zid = %(zid)s"""            
        if self.zid < 0:
            mz = self.max_zid() 
            sqlargs['zid'] = str(mz)
            sql = ins % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        else:
            sql = updt % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        self.p.zatwierdz()
    
    
        
    def zapisz(self):
        print 'zapisuje'
        if self.czy_zm:
            zm = {1:'T',0:'N'}
            sqlargs = {'sid':str(self.stan.sid),'istn':zm[self.istn],'stal':zm[self.stal],'ludz':zm[self.ludz],'natu':zm[self.nat],
                    'pryw':zm[self.pryw],'spol':zm[self.spol],'dodat':self.dodat,'zid':str(self.zid)}
            self.moddb(sqlargs)
        else:
            print 'ZAGROZENIE: brak zmian'
        