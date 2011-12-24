'''
Created on Jul 8, 2011

@author: milosz
'''
# informacja o polozeniu okreslonym w momencie wejscia. Odnosi sie do okreslonego stanowiska

class Polozenie:
    czy_zm = False
    nowe = False
    modstr = """select * from azp_zmien_polozenie(%d,'%s','%s','%s','%s','%s','%s','%s','%s',
                '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s', %d)"""
    def __init__(self,stan,con,td=None):
        if td is not None and len(td) == 23:
            zm = {'T':1,'N':0}
            self.nadm,self.morze,self.plaza,self.mierz,self.skarpa,self.wal = zm[td[2]],zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]]
            self.dd,self.woda,self.terden,self.ternad,self.terwyz,self.brz = zm[td[8]],zm[td[9]],zm[td[10]],zm[td[11]],zm[td[12]],zm[td[13]]
            self.md,self.dnod,self.stokd,self.krawd = zm[td[14]],zm[td[15]],zm[td[16]],zm[td[17]]
            self.pd,self.rown,self.fal,self.pagor,self.gorz = zm[td[18]],zm[td[19]],zm[td[20]],zm[td[21]],zm[td[22]]
            self.pid = td[0]
            #self.jedn = td[2].decode('utf-8')
            #self.morze,self.plaza,self.mierz,self.skarpa,self.wal,self.woda,self.terden = zm[td[3]],zm[td[4]],zm[td[5]],zm[td[6]],zm[td[7]],zm[td[8]],zm[td[9]]
            #self.ternad,self.terwyz,self.dnod,self.stokd,self.krawd,self.rown,self.fal = zm[td[10]],zm[td[11]],zm[td[12]],zm[td[13]],zm[td[14]],zm[td[15]],zm[td[16]]
            #self.pagor,self.gorz = zm[td[17]],zm[td[18]]
            #self.pid = td[0]
        else:
            self.nadm,self.morze,self.plaza,self.mierz,self.skarpa,self.wal = 0,0,0,0,0,0
            self.dd,self.woda,self.terden,self.ternad,self.terwyz,self.brz = 0,0,0,0,0,0
            self.md,self.dnod,self.stokd,self.krawd = 0,0,0,0
            self.pd,self.rown,self.fal,self.pagor,self.gorz = 0,0,0,0,0,
            self.pid = -1
            self.nowe = True
        self.p = con
        self.stan = stan

    def zmien(self,var,val):
        if hasattr(self,var) and getattr(self,var,None) != val:
            setattr(self,var,val)
            self.czy_zm = True
            
    def max_pid(self):
        max_id = "select coalesce(max(pid),0)+1 as nast from polozenia"
        mt = self.p.wykonaj(max_id)
        return mt[0][0]
            
        
    def moddb(self,sqlargs):
        #(nast,stanowisko,obser,obpole,nasyc,gest,powierz,centrycz)
        ins = """ insert into polozenia values(%(pid)s,%(sid)s,'%(nadm)s','%(morz)s','%(plaz)s','%(mierz)s','%(skarp)s','%(wal)s',
                        '%(duzd)s','%(wod)s','%(terden)s','%(ternad)s','%(terwy)s','%(brzeg)s',
                        '%(mald)s','%(dnod)s','%(stokd)s','%(krawd)s',
                        '%(pozad)s','%(rown)s','%(fal)s','%(pagor)s','%(gorz)s');"""
        #update obszary set obserwacja = obser, pole = obpole, nasycenie = nasyc, gestosc = gest,
        #powierzchnia = powierz, centrycznosc = centrycz where oid = obsz_id;
        updt = """UPDATE polozenia SET nadmorska='%(nadm)s', morze='%(morz)s', plaza='%(plaz)s', mierzeja='%(mierz)s',
        skarpa='%(skarp)s', wal_wydma='%(wal)s',duza_dol='%(duzd)s',woda='%(wod)s',terasa_denna='%(terden)s', 
        terasa_nadzalew='%(ternad)s',terasa_wyzsza='%(terwy)s',brzeg_wys='%(brzeg)s', mala_dol='%(mald)s',dno_doliny='%(dnod)s', 
        stok_doliny='%(stokd)s', kraw_doliny='%(krawd)s', poza_dol='%(pozad)s',rownina='%(rown)s', 
        obsz_falisty='%(fal)s', obsz_pagor='%(pagor)s',obszar_gorz='%(gorz)s'
     WHERE pid=%(pid)s"""            
        if self.pid < 0:
            mp = self.max_pid() 
            sqlargs['pid'] = str(mp)
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
            sqlargs = {'sid':str(self.stan.sid),'nadm':zm[self.nadm],'morz':zm[self.morze],'plaz':zm[self.plaza],'mierz':zm[self.mierz],
                       'skarp':zm[self.skarpa],'wal':zm[self.wal],'duzd':zm[self.dd],'wod':zm[self.woda],'terden':zm[self.terden],
                       'ternad':zm[self.ternad],'terwy':zm[self.terwyz],'brzeg':zm[self.brz],'mald':zm[self.md],
                       'dnod':zm[self.dnod],'stokd':zm[self.stokd],'krawd':zm[self.krawd],'pozad':zm[self.pd],'rown':zm[self.rown],
                       'fal':zm[self.fal],'pagor':zm[self.pagor],'gorz':zm[self.gorz],'pid':str(self.pid)}
            self.moddb(sqlargs)
        else:
            print 'POLOZENIE: brak zmian'