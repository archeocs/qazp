# -*- coding: utf-8 -*-

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

class Polaczenie(object):
    
    PG = 1
    LITE = 2

    def __init__(self, con, typ):
        self._con = con
        self._tc = typ
        if typ == self.PG:
            self.nrep = '%%(%s)s'
            self.rep = '%s'
        elif typ == self.LITE:
            self.nrep = ':%s'
            self.rep = '?'

    def zatwierdz(self):
        self._con.commit()
        
    def wycofaj(self):
        self._con.rollback()
        
    def zakoncz(self):
        self._con.close()
        self._con = None
    
    def wykonaj(self, sql, vp=[], zatw=True):
        self.prep(sql).wykonaj(vp,zatw)
        
    def wszystkie(self, sql, vp=[], f=None):
        return self.prep(sql).wszystkie(vp,f)
        
    def jeden(self, sql, vp=[], f=None):
        return self.prep(sql).jeden(vp,f)
    
    def prep(self, sql, params=[]):
        ts = sql
        for p in params:
            ts = ts.replace('#',self.nrep%p,1)
        if params:
            if ts.rfind('#') > -1:
                #print 'zbyt malo parametrow'
                return None
            return Polecenie(self._con,ts)
        ts = ts.replace('#',self.rep)
        return Polecenie(self._con,ts)

class Polecenie(object):
    
    def __init__(self, con, prepSql):
        self._ps = prepSql
        self._con = con    
    
    def wykonaj(self, params=[], zatwierdz=True): # mapa albo lista
        cur = self._con.cursor()
        cur.execute(self._ps, params)
        cur.close()
        if zatwierdz:
            self._con.commit()
    
    def wszystkie(self, params=[], f=None):
        cur = self._con.cursor()
        cur.execute(self._ps, params)
        ret = []
        for r in cur.fetchall():
            if f is not None:
                ret.append(f(r))
            else:
                ret.append(r)
        cur.close()
        #print ret
        return ret
    
    def jeden(self, params=[], f=None):
        cur = self._con.cursor()
        cur.execute(self._ps, params)
        r = cur.fetchone()
        cur.close()
        if f is not None:
            return f(r)
        return r
        
def getLite(db):
    import sqlite3
    return Polaczenie(sqlite3.connect(db),Polaczenie.LITE)