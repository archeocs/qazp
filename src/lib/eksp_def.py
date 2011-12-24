'''
Created on Jul 8, 2011

@author: milosz
'''
# informacja o ekspozycji stanowiska
class Ekspozycja:
    # tab_dane = [eksponowany,kraw_stok,sfal_cypel,cypl,wal_garb,okrezna,podst_stoku,dolina_niecka,kotl_zagl,jaskinia,eid]
    czy_zm = False
    nowe = False
    #modstr = """select * from azp_zmien_ekspozycje(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
    #                '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d)"""
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
        
    def max_eid(self):
        max_id = "select coalesce(max(eid),0)+1 as nast from ekspozycje"
        mt = self.p.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        ins = """ insert into ekspozycje values(%(eid)s,%(stan)s,'%(eksp)s','%(kraw)s','%(sfal)s',
                                                '%(cypel)s','%(wal)s','%(okrez)s','%(oslo)s', %(stok)s','%(dolina)s', 
                                                '%(kotl)s','%(jask)s','%(szczeg)s','%(n)s','%(ne)s','%(e)s',
                                                '%(se)s', '%(s)s', '%(sw)s', '%(w)s', '%(nw)s')"""
        
        updt = """update ekspozycje set eksponowany='%(eksp)s',kraw_stok='%(kraw)s',sfal_cypel='%(sfal)s',
                cypl='%(cypel)s',wal_garb='%(wal)s',okrezna='%(okrez)s',
                podst_stoku='%(stok)s',dolina_niecka='%(dolina)s',osloniety='%(oslo)s',
                kotl_zagl='%(kotl)s',jaskinia='%(jask)s', forma_szczegolna='%(szczeg)s',
                kier_n='%(n)s',kier_ne='%(ne)s',kier_e='%(e)s',kier_se='%(se)s',kier_s='%(s)s',kier_sw='%(sw)s',kier_w='%(w)s', 
                kier_nw='%(nw)s'
                 where eid=%(eid)s; """            
        if self.eid < 0:
            me = self.max_eid() 
            sqlargs['eid'] = str(me)
            sql = ins % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        else:
            sql = updt % sqlargs
            print sql
            self.p.wykonaj(sql,False)
        self.p.zatwierdz()
            
        
    def zmien(self,var,val):
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_zm = True
        
    def zapisz(self):
        if self.czy_zm:
            zm = {1:'T',0:'N'}
            sqlargs = {'stan':str(self.stan.sid),'eid':str(self.eid),'eksp':zm[self.czy_eksp],'kraw':zm[self.kraw],
                       'sfal':zm[self.sfal],'cypel':zm[self.cypel],'wal':zm[self.wal],'okrez':zm[self.okrez],'oslo':zm[self.oslo],
                       'stok':zm[self.stok],'dolina':zm[self.dolina],'kotl':zm[self.kotl],'jask':zm[self.jask],'szczeg':self.szczegolna,
                       'n':zm[self.n],'ne':zm[self.ne],'e':zm[self.e],'se':zm[self.se], 's':zm[self.s],'sw':zm[self.sw],
                       'w':zm[self.w],'nw':zm[self.nw]}
            self.moddb(sqlargs)
            #===================================================================
            # self.p.wykonaj(self.modstr % (self.stan.sid,zm[self.czy_eksp],zm[self.kraw],zm[self.sfal],zm[self.cypel],
            #                              zm[self.wal],zm[self.okrez],zm[self.oslo],zm[self.stok],zm[self.dolina],zm[self.kotl],
            #                              zm[self.jask],self.szczegolna,zm[self.n],zm[self.ne],zm[self.e],zm[self.se],
            #                              zm[self.s],zm[self.sw],zm[self.w],zm[self.nw],self.eid))
            #===================================================================
        else:
            print 'EKSPOZYCJA brak zmian'