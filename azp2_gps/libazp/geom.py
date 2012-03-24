'''
Created on Mar 20, 2012

@author: milosz
'''

class Feature(object):
    
    def wkt(self):
        raise Exception('Brak implementacji')
    
    def __unicode__(self):
        return self.wkt()
    
    def wkb(self,srid=4326):
        return u"ST_GeomFromText('%s',%d)" % (self.wkt(),srid)

class Point(Feature):
    
    def __init__(self, lon, lat): # lon - dlugosc, lat - szerokosc
        self.lon = lon
        self.lat = lat
    
    def wkt(self):
        return u'POINT(%s,%s)' % (self.lon, self.lat)
    
    def fmt(self,f=u'%s %s'):
        return f % (self.lon, self.lat)

class GeomError(Exception):
    
    def __init__(self,err):
        self.msg = err
        
    def __unicode__(self):
        return unicode(self.msg)
    
class Line(Feature):
    
    def __init__(self,points=[]):
        if points:
            if isinstance(points[0],tuple):
                self.points = []
                for p in points:
                    self.points.append(Point(p[0],p[1]))
            elif isinstance(points[0],Point):
                self.points = points
            else:
                raise GeomError(u'Nieprawidlowy typ '+type(points[0]))
        else:
            self.points = []
    
    def wkt(self):
        geoms = u''
        fmt_pt = u', %s %s'
        for p in self.points:
            geoms += p.fmt(fmt_pt)
        return u'LINESTRING(%s)' % geoms[2:]
            
    def add_point(self,pt):
        if isinstance(pt,tuple):
            self.points.append(Point(pt[0],pt[1]))
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
        
def geom_str_sql(param,gsrid=4326,tsrid=2180):
    return 'ST_Transform(ST_GeomFromText(%('+param+')s,%d),%d)' % (gsrid,tsrid)