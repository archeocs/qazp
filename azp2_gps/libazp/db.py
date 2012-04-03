# LIBAZP - klasy AZP2
# (c) Milosz Piglas 2012 Wszystkie prawa zastrzezone

#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
# 
#      * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following disclaimer
#  in the documentation and/or other materials provided with the
#  distribution.
#      * Neither the name of Milosz Piglas nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
    
class Database(object):
    
    def set_con(self,con):
        self._con = con
        
    def get_cursor(self):
        return self._con.cursor()
    
    def commit(self):
        try:
            self._con.commit()
        except Exception, e:
            raise DbError(u"Nieudane zatwierdzenie",e)
        
    def rollback(self):
        try:
            self._con.rollback()
        except Exception, e:
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
        except Exception, e:
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

def get_lite_db(baza):
    return Spatialite(baza)
    
class Spatialite(Database):
    
    foto = True
    geom = True
    def __init__(self,baza):
        Database.__init__(self)
        try:
            import pyspatialite as db
        except ImportError:
            import sqlite3 as db
            self.geom = False
        self.set_con(db.connect(baza))
        
def get_postgis_db(baza='azp2',user='postgres',pswd='postgres',host='localhost',port='5432'):
    return Postgis(baza,user,pswd,host,port)
    
class Postgis(Database):
    
    MIN_VER = '2.4.2'
    foto = True
    geom = True # True oznacza ze mozna uzywa funkcji OpenGIS
    def __init__(self,baza='azp2',user='postgres',pswd='postgres',host='localhost',port='5432'):
        Database.__init__(self)
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
        self.set_con(psycopg2.connect(database=baza,host=host,port=port,user=user,password=pswd))