# -*- coding: utf-8 -*-

# polaczenie z baza postgresql

from pol import Polaczenie
from zestawienia import Zestawienie

class PolPg(Polaczenie):
    
    p = None
    def __init__(self,baza,usr,pswd,hn=None,host_port='5432'):
        import psycopg2
        self.p = psycopg2.connect(database=baza,host=hn,port=host_port,user=usr,password=pswd)
        
    def get_stanowiska(self,where):
        #stlista = [] 
        c = self.p.cursor()
        c.execute("""select sid,rodzaj,arkusz,nr_arkusz,miejscowosc,nr_miejscowosc,coalesce(astext(wspolrzedne),'') 
                    as geom,cast(data as date),autor,lokalizacja from stanowiska """+where)
        sts = c.fetchall()
        #for s in sts:
        #    stlista.append(Stanowisko(s))D
        c.close()
        #return stlista
        return sts
        
    def get_arkusze(self):
        arklista = []
        c = self.p.cursor()
        c.execute('select distinct arkusz from stanowiska order by arkusz')
        arks = c.fetchall()
        for a in arks:
            arklista.append(a[0])
        c.close()
        return arklista
        
    def get_nrark(self,a):
        nrlista = []
        c = self.p.cursor()
        c.execute("select distinct nr_arkusz from stanowiska where arkusz = '%s' order by nr_arkusz asc"%a)
        nrs = c.fetchall()
        for n in nrs:
            nrlista.append(n[0])
        c.close()
        return nrlista
        
    def get_kryteria(self):
        c = self.p.cursor()
        c.execute('select distinct arkusz, nr_arkusz from stanowiska order by arkusz asc')
        krs = c.fetchall()
        #for k in krs:
        #    klista.append(Wiersz(k))
        c.close()
        return krs
        #return klista
        
    def wykonaj(self,sql,sel=True):
        c = self.p.cursor()
        try:
            c.execute(sql)
            if sel:
                wyn = c.fetchall()
                c.close()
                return wyn
            else:
                return None
        except Exception, e:
            self.p.rollback()
            print e
            return None
            
    def lokal_info(self,lokal_id):
        c = self.p.cursor()
        sql = """SELECT L.ARKUSZ,L.NR_ARKUSZ,M.NAZWA AS "MIEJSCOWOSC", coalesce(M.SID,-1) AS "MID", 
                L.NR_MIEJSCOWOSC, G.NAZWA AS "GMINA", coalesce(G.SID,-1) AS "GID", 
                P.NAZWA AS "POWIAT", coalesce(P.SID,-1) AS "PID", W.NAZWA AS "WOJEWODZTWO", coalesce(W.SID,-1) AS "WID"
                FROM LOKALIZACJE L JOIN MIASTA_SLO M ON L.MIEJSCOWOSC = M.SID 
                                   JOIN GMINY_SLO G ON L.GMINA = G.SID 
                                   LEFT OUTER JOIN POWIATY_SLO P ON L.POWIAT = P.SID
                                   LEFT OUTER JOIN WOJEWODZTWA_SLO W ON L.WOJEWODZTWO = W.SID 
                                   where L.lid = %d""" % lokal_id
        c.execute(sql)
        wyn = c.fetchall()
        c.close()
        if len(wyn) == 1:
            return wyn[0]
        elif len(wyn) == 0:
            return None
        else:
            print "len(lokalizacje) > 1 !!!!"
            return None
        
    
    def lokal_lid(self,ark,nrark):
        sql = "SELECT LID FROM LOKALIZACJE WHERE ARKUSZ = '%s' AND NR_ARKUSZ = '%s'" % (ark,nrark)
        c = self.p.cursor()
        c.execute(sql)
        wyn = c.fetchall()
        c.close()
        if len(wyn) == 1:
            return wyn[0][0]
        elif len(wyn) == 0:
            return None
        else:
            print "len(lokalizacje) > 1!!!"
            return None
        
    
    def fakty_info(self,stan):
        c = self.p.cursor()
        sql = """ select mid,coalesce(epoka,0),coalesce(kultura,0),coalesce(funkcja,0),ceramika,kamien,metal, 
                    coalesce(e.nazwa,'Nieokreślona') as "en", coalesce(k.nazwa,'Nieokreślona') as "kn", coalesce(f.nazwa,'Nieokreślona') 
                    as "fn",m.masowy,m.wyodrebniony 
                    from materialy m left outer join epoki_slo e on m.epoka = e.sid left outer join kultury_slo k on m.kultura = k.sid 
                    left outer join funkcje_slo f on m.funkcja = f.sid  where
                    stanowisko = %d order by mid""" % stan.sid
        c.execute(sql)
        fks = c.fetchall()
        tf = []
        for f in fks:
            tf.append(f)
        c.close()
        return tf
        
    def eksp_info(self,stan):
        c = self.p.cursor()
        sql = """select * from ekspozycje where stanowisko = %d""" % stan.sid
        c.execute(sql)
        ekst = c.fetchall()
        if len(ekst) == 0:
            return None
        elif len(ekst) == 1:
            return ekst[0] #Ekspozycja(stan,self.p,ekst)
        else:
            print "len(ekpozycje) > 1!!!"
            return None      
    
    def obszar_info(self,stan):
        c = self.p.cursor()
        sql = """ select obserwacja,pole,nasycenie,gestosc, powierzchnia,oid,centrycznosc from obszary where stanowisko = %d"""%stan.sid
        c.execute(sql)
        ekst = c.fetchall()
        if len(ekst) == 0:
            return None
        elif len(ekst) == 1:
            return ekst[0]
        else:
            return None
            
    def teren_info(self,stan):
        c = self.p.cursor()
        sql = """select * from tereny where stanowisko = %d""" % stan.sid
        c.execute(sql)
        ekst = c.fetchall()
        if len(ekst) == 0:
            return None
        elif len(ekst) == 1:
            return ekst[0] #Teren(stan,self.p,ekst)
        else:
            print "len(teren) > 1!!!"
            return None                                
    
    def polozenie_info(self,stan):
        c = self.p.cursor()
        sql = """select * from polozenia where stanowisko = %d""" % stan.sid
        c.execute(sql)
        ekst = c.fetchall()
        if len(ekst) == 0:
            return None
        elif len(ekst) == 1:
            return ekst[0] #Teren(stan,self.p,ekst)
        else:
            print "len(polozenie) > 1!!!"
            return None 
    
    def wnioski_info(self,stan):
        c = self.p.cursor()
        sql = """ select * from wnioski where stanowisko = %d """ % stan.sid
        c.execute(sql)
        ekst = c.fetchall()
        if len(ekst) == 0:
            return None
        elif len(ekst) == 1:
            return ekst[0]
        else:
            print "len(wnioski) > 1"
            return None
    
    def zagroz_info(self,stan):
        c = self.p.cursor()
        sql = """ select zid,istnieje,stale,ludzie,natura,prywatny,spoleczny,dodatkowe from zagrozenia 
                where stanowisko = %d """ % stan.sid
        c.execute(sql)
        ekst = c.fetchall()
        if len(ekst) == 0:
            return None
        elif len(ekst) == 1:
            return ekst[0]
        else:
            print "len(zagrozenia) > 1"
            return None
    
    def utworz_zestawienie(self,sql):
        return Zestawienie(self.p,sql)          
        
    def zatwierdz(self):
        self.p.commit()
        
    def wycofaj(self):
        self.p.rollback()