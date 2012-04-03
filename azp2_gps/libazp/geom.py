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

def point2D(lon,lat):
    return u'POINT(%s %s)' % (lon,lat)

def point3D(lon,lat,elev):
    return u'POINT(%s %s %s)' % (lon,lat,elev)

def geom2D(lon,lat,fmt=u'%s %s'):
    return fmt % (lon,lat)

def geom3D(lon,lat,elev,fmt=u'%s %s %s'):
    return fmt % (lon,lat,elev)

class Feature(object):
    
    def wkt(self):
        raise Exception('Brak implementacji')
    
    def __unicode__(self):
        return self.wkt()
    
    def wkb(self,srid=4326):
        return u"ST_GeomFromText('%s',%d)" % (self.wkt(),srid)
    
    def get_dim(self):
        return 2

class Point(Feature):
    
    __pt_fmt = u'POINT(%s %s)'
    __vals_fmt = []
    def __init__(self, lon, lat, dim=2, elev=''): # lon - dlugosc, lat - szerokosc
        self.lon = lon
        self.lat = lat
        self.dim = dim
        self.elev = elev
        self.__vals_fmt = [lon,lat,elev]
        if self.dim == 3:
            self.__pt_fmt = u'POINT(%s %s %s)'
        elif self.dim != 2:
            raise GeomError('Nieprawidlowy wymiar '+self.dim)
    
    def set_elev(self,e):
        if self.dim == 3:
            self.elev = e
            self.__vals_fmt[2] = e
    
    def wkt(self):
        try:
            return self.__pt_fmt % tuple(self.__vals_fmt[:self.dim])
        except TypeError, e:
            raise GeomError('Nieprawidlowy format '+str(e))
        
    def get_dim(self):
        return self.dim
    
    def fmt(self,f=u'%s %s'):
        try:
            #print self.dim, self.__vals_fmt[:self.dim]
            #raw_input('dalej')
            return f % tuple(self.__vals_fmt[:self.dim])
        except TypeError, e:
            raise GeomError('Nieprawidlowy format '+str(e))
        
    def __eq__(self,p):
        return self.lon == p.lon and self.lat == p.lat and self.elev == p.elev
    
    def __ne__(self,p):
        return self.lon != p.lon or self.lat != p.lat or self.elev != p.elev
    
class GeomError(Exception):
    
    def __init__(self,err):
        self.msg = err
        
    def __unicode__(self):
        return unicode(self.msg)
    
class Line(Feature):
    
    __pt_fmt = ', %s %s'
    def __init__(self,points=[],dim=2):
        self.dim = dim
        if self.dim == 3:
            self.__pt_fmt = ', %s %s %s'
        if points:
            if isinstance(points[0],tuple):
                self.points = []
                for p in points:
                    if dim == 2:
                        self.points.append(Point(p[0],p[1]))
                    elif dim == 3:
                        self.points.append(Point(p[0],p[1],dim=dim,elev=p[2]))
            elif isinstance(points[0],Point):
                self.points = points
            else:
                raise GeomError(u'Nieprawidlowy typ '+type(points[0]))
        else:
            self.points = []
            
    def get_dim(self):
        return self.dim
    
    def wkt(self):
        geoms = u''
        for p in self.points:
            #print self.__pt_fmt
            geoms += p.fmt(self.__pt_fmt)
        return u'LINESTRING(%s)' % geoms[2:]
            
    def add_point(self,pt):
        if isinstance(pt,tuple):
            if self.dim == 2:
                self.points.append(Point(pt[0],pt[1]))
            elif self.dim == 3:
                self.points.append(Point(pt[0],pt[1],dim=self.dim,elev=pt[2]))
        elif isinstance(pt,Point):
            self.points.append(pt)
        else:
            raise GeomError(u'Nieprawidlowy typ '+type(pt))                
        
    def add_point_obj(self,pt):
        self.points.append(pt)
   
    def first(self):
        if self.points:
            return self.points[0]
        return None
    
    def last(self):
        if self.points:
            return self.points[-1]
        return None
        
    def count_pts(self):
        return len(self.points)
    
    def __eq__(self,x):
        for (i,j) in zip(self.points,x.points):
            if i != j:
                print 'p1', unicode(i), 'p2',unicode(j)
                return False
        return True


POSTGIS_FMT = '%%(%s)s'
LITE_FMT = ':%s'
        
def geom_str_sql(param,gsrid=4326,tsrid=2180,fmt=POSTGIS_FMT):
    pf = fmt % param
    return 'ST_Transform(ST_GeomFromText('+pf+',%d),%d)' % (gsrid,tsrid)
