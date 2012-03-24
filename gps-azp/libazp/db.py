'''
Created on Mar 20, 2012

@author: milosz
'''
from storm.databases.postgres import psycopg2
import logging

class DbError(object):
    
    def __init__(self,msg,err):
        self.msg = msg
        self.err = err
        
    def __unicode__(self):
        return unicode(self.msg)

class RowFactory(object):
    
    def getRow(self,indeks,dbrow):
        return tuple(dbrow)
    
class Postgis(object):
    
    MIN_VER = '2.4.2'
    foto = True
    geom = True # True oznacza ze mozna uzywa funkcji OpenGIS
    def __init__(self,baza='azp2',user='postgres',pswd='postgres',host='localhost',port='5432'):
        logging.basicConfig(level=logging.INFO)
        try:
            import psycopg2
            v = psycopg2.__version__.split()[0].strip()
            if len(v) < len(self.MIN_VER):
                self.foto = False
                logging.warn("min > ins: %s > %s"%(self.MIN_VER,v))
            elif len(v) == len(self.MIN_VER) and v < self.MIN_VER:
                self.foto = False
                logging.warn("min > ins: %s > %s"%(self.MIN_VER,v))
        except ImportError, e:
            raise DbError('Nieudane polaczenie z baza postgis ',e)
        self._con = psycopg2.connect(database=baza,host=host,port=port,user=user,password=pswd)
        
    def get_cursor(self):
        return self._con.cursor()
    
    def commit(self):
        try:
            self._con.commit()
        except psycopg2.Error, e:
            raise DbError(u"Nieudane zatwierdzenie",e)
        
    def rollback(self):
        try:
            self._con.commit()
        except psycopg2.Error, e:
            raise DbError(u"Nieudane wycofanie",e)
        
    def _execute(self,cmd,args={},cursor=None,raise_err=False):
        c = cursor
        close_c = False
        if c is None:
            c = self.get_cursor()
            close_c = True
        try:
            c.execute(cmd,args)
            return c
        except psycopg2.Error, e:
            if raise_err:
                if close_c:
                    c.close()
                raise DbError(u"Nieudane wykonanie polecenia "+cmd+" "+str(args), e)
            else:
                self.rollback()
                logging.error(str(e)+": Nieudane wykonanie polecenia "+cmd+" "+str(args))
                if close_c:
                    c.close()
                    return None
    
    def fetch(self,cmd,args={},cursor=None,raise_err=False,row_factory=RowFactory()):
        c = self._execute(cmd, args, cursor, False, raise_err)
        rows = []
        for (ri,r) in enumerate(c.fetchall()):
            rows.append(row_factory.getRow(ri,r))
        if cursor is None:
            cursor.close()
        return rows
    
    def update(self,cmd,args={},cursor=None,raise_err=False,commit=False):
        c = self._execute(cmd, args, cursor, raise_err)
        if c is not None:
            if commit:
                self._con.commit()
            if cursor is None:
                c.close()
            return True
        return False