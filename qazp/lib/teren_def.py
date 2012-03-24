'''
Created on Jul 8, 2011

@author: milosz
'''
# informacja o terenie

class Teren:
    # tab_dane = [tid,sid,pole_orne,sad,torf,nieuzytek,park,laka,bagno,las,zabud,niezabud,srednio_zabud, okresl bliz
    nowe = False
    czy_zm = False
    modstr = "select * from azp_zmien_teren(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d)"
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 14:
            zm = {'T':1,'N':0}
            self.tid = td[0]
            self.orne,self.sad,self.pryw,self.spol,self.park,self.laka = zm[td[2]],zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]]
            self.przem,self.las,self.zab,self.niezab,self.srezab = zm[td[8]],zm[td[9]],zm[td[10]],zm[td[11]],zm[td[12]]
            self.bliz = td[13].decode('utf-8')
            #self.tid = td[0]
        else:
            self.orne,self.sad,self.pryw,self.spol,self.park,self.laka = 0,0,0,0,0,0
            self.przem,self.las,self.zab,self.niezab,self.srezab = 0,0,0,0,0,
            self.bliz = ""
            self.tid = -1
            self.nowe = True
        self.p = con
        self.stan = stan
    
    def zmien(self,var,val):
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_zm = True
    
    def max_tid(self):
        max_id = "select coalesce(max(tid),0)+1 as nast from tereny"
        mt = self.p.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        #(nast,stanowisko,obser,obpole,nasyc,gest,powierz,centrycz)
        ins = """ insert into tereny values(%(tid)s,%(sid)s,'%(pole)s','%(sa)s','%(pryw)s','%(spol)s','%(par)s','%(lak)s',
                        '%(przem)s','%(las)s','%(zab)s','%(niezab)s','%(srezab)s','%(blizsze)s')"""
        #update obszary set obserwacja = obser, pole = obpole, nasycenie = nasyc, gestosc = gest,
        #powierzchnia = powierz, centrycznosc = centrycz where oid = obsz_id;
        updt = """update tereny set pole_orne='%(pole)s',sad='%(sa)s',prywatny='%(pryw)s',spoleczny='%(spol)s',
                park='%(par)s',laka='%(lak)s',przemyslowy='%(przem)s',las='%(las)s',zabud='%(zab)s',niezabud='%(niezab)s',
                srednio_zabud='%(srezab)s',okresl_blizsze='%(blizsze)s' where tid=%(tid)s"""            
        if self.tid < 0:
            mt = self.max_tid() 
            sqlargs['tid'] = str(mt)
            sql = ins % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        else:
            sql = updt % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        self.p.zatwierdz()
    
    
    
    def zapisz(self):
        if self.czy_zm:
            zm = {1:'T',0:'N'}
            sqlargs = {'sid':str(self.stan.sid),'pole':zm[self.orne],'sa':zm[self.sad],'pryw':zm[self.pryw],'spol':zm[self.spol],
                    'par':zm[self.park],'lak':zm[self.laka],'przem':zm[self.przem],'las':zm[self.las],'zab':zm[self.zab],
                    'niezab':zm[self.niezab],'srezab':zm[self.srezab],'blizsze':self.bliz,'tid':str(self.tid)}
            self.moddb(sqlargs)
        else:
            print "TEREN: brak zmian"