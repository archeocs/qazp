'''
Created on Jul 23, 2011

@author: milosz
'''

class Zestawienie(object):
    
    def __init__(self, pol, sql=None):
        self.pol = pol
        self.sql = sql
        self.wykonane = False
        
    def set_sql(self,sql):
        self.sql = sql
        
    def wykonaj(self,params = {}):
        self.cursor = self.pol.cursor()
        try: 
            self.cursor.execute(self.sql)
            self.zestpola = []
            for koldesc in self.cursor.description:
                self.zestpola.append((koldesc[0],koldesc[1]))
            return None   
        except Exception as e:
            self.pol.rollback()
            #print dir(e)
            return unicode(e)
    
    def nazwy_pol(self):
        return [p[0].decode('utf-8') for p in self.zestpola]
    
    def pola(self):
        return self.zestpola
    
    def usun_cursor(self):
        self.cursor.close()
    
    def _tounicode(self,val):
        if isinstance(val, str):
            return val.decode('utf-8')
        else:
            return unicode(val)
    
    def wiersze(self):
        for wiersz in self.cursor.fetchall():
            yield map(self._tounicode,wiersz)