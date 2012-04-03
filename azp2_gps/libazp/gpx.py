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

from xml.parsers.expat import ParserCreate
from geom import Line,Point
from geom import geom2D, geom3D,point2D,point3D
import time

class GpxPoint(object):
    
    lon,lat,ele = '','',''
    time,name,cmt = '','',''
    desc,type='',''
    dim=2
    _strp_fmt = '%Y-%m-%dT%H:%M:%S'
    
    def __init__(self,lon,lat,elev='0',dim=2,atrs={}):
        self.lon = lon
        self.lat = lat
        self.ele = elev
        self.dim = dim
        for (k,v) in atrs.iteritems():
            setattr(self, k, v)
            
    def wkt(self):
        if self.dim == 2:
            return point2D(self.lon, self.lat)
        elif self.dim == 3:
            return point3D(self.lon,self.lat,self.ele)
        return None
    
    def fmt(self,f):
        if self.dim == 2:
            return geom2D(self.lon, self.lat, f)
        elif self.dim == 3:
            return geom3D(self.lon, self.lat, self.ele, f)
        return None
    
    def to_point(self):
        if self.dim == 2:
            return Point(self.lon,self.lat)
        elif self.dim == 3:
            return Point(self.lon,self.lat,dim=self.dim,elev=self.ele)
        return None
    
    def get_time(self):
        return self.time.replace('Z','+0100')
    
    def timestamp(self):
        return time.mktime(time.strptime(self.time.replace('Z',''),self._strp_fmt))
    
def distr(values):
    m = sum(values) / len(values)
    s = pow(sum([pow(v-m, 2) for v in values]) / len(values), 0.5)
    return (m,s)
        
class GpxPointsList(object):
    
    points = []
    
    def __init__(self,dim=2,pts=[]):
        self.dim = dim
        self.points = []
        self.points.extend(pts)
        
    def add_point(self,wp):
        self.points.append(wp)
        
    def pt_list(self):
        if self.dim == 2:
            return [Point(p.lon,p.lat) for p in self.points]
        elif self.dim == 3:
            return [Point(p.lon,p.lat,dim=self.dim,elev=p.ele) for p in self.points]
        else:
            return []
        
    def line(self):
        return Line(self.pt_list(),dim=self.dim)
    
    def first(self):
        return self.points[0]
    
    def last(self):
        return self.points[-1]
    
    def count(self):
        return len(self.points)
    
    def min_time(self):
        return min(self.points,key=lambda x: x.time).time
    
    def max_time(self):
        return max(self.points,key=lambda x: x.time).time
    
    def time_deltas(self):
        t = self.points[0].timestamp()
        deltas = []
        for p in self.points[1:]:
            deltas.append(abs(t-p.timestamp()))
            t = p.timestamp()
        return deltas
    
    def __add__(self,pts):
        if isinstance(pts, GpxPointsList):
            return GpxPointsList(self.dim,self.points+pts.points)
        
class WayPoints(object):
     
    chname,chval = None,''
    def __init__(self,dim=2):
        self.dim = dim
        self.wpts = GpxPointsList(dim)
        
    def elem_start(self,name,atrs):
        if name == 'wpt':
            self.cur_pt = GpxPoint(lon=atrs['lon'],lat=atrs['lat'],dim=self.dim)
        elif not self.chname and not self.chval:
            self.chname = name
            self.chval = ''
    
    def chdata(self,txt):
        if self.chname and self.cur_pt:
            self.chval += txt
            
    def elem_end(self,name):
        if name == 'wpt' and self.cur_pt:
            self.wpts.add_point(self.cur_pt)
            self.chname=None
            self.chval=None
        elif self.chname and self.chval:
            setattr(self.cur_pt, self.chname, self.chval)
            self.chname = None
            self.chval = None
            
    def create(self,fn):
        parser = ParserCreate()
        parser.StartElementHandler = self.elem_start
        parser.EndElementHandler = self.elem_end
        parser.CharacterDataHandler = self.chdata
        parser.ParseFile(open(fn,'r'))
            
class TrackPoints(object):
    
    chname,chval = None,''
    segments = []
    track = False
    cur_seg, cur_pt = None,None
    def  __init__(self,dim=2):
        self.dim = dim
        self.segments = []
    
    def elem_start(self,name,atrs):
        if name == 'trk':
            self.track = True
        elif name == 'trkseg' and self.track and not self.cur_seg:
            self.cur_seg = GpxPointsList(self.dim)
        elif name == 'trkpt' and self.cur_seg and not self.cur_pt:
            self.cur_pt = GpxPoint(lon=atrs['lon'],lat=atrs['lat'],dim=self.dim)
        elif not self.chname and not self.chval and self.cur_pt:
            self.chname = name
            self.chval = ''

    def chdata(self,txt):
        if self.chname and self.cur_pt:
            self.chval += txt
            #self.chval = txt
                
    def count(self):
        return len(self.segments)
            
    def elem_end(self,name):
        if name == 'trkpt' and self.cur_seg and self.cur_pt:
            self.cur_seg.add_point(self.cur_pt)
            self.cur_pt = None
            self.chname = None
            self.chval = None
        elif name == 'trkseg' and self.cur_seg and not self.cur_pt:
            if self.cur_seg.count() > 1:
                self.segments.append(self.cur_seg)
            self.cur_seg = None
        elif name == 'trk' and not self.cur_seg and not self.cur_pt:
            self.track = False
        elif self.chname and self.chval != '' and self.cur_pt:
            setattr(self.cur_pt, self.chname, self.chval)
            self.chname = None
            self.chval = None
            
    def concat(self,ind=[]):
        new_list = []
        if ind:
            for i in ind:
                new_list.extend(self.segments[i].points)
        else:
            for s in self.segments:
                new_list.extend(s.points)
        return GpxPointsList(dim=self.dim,pts=new_list)
    
    def get_segments(self):
        return self.segments
            
    def create(self,fn):
        parser = ParserCreate()
        parser.StartElementHandler = self.elem_start
        parser.EndElementHandler = self.elem_end
        parser.CharacterDataHandler = self.chdata
        parser.ParseFile(open(fn,'r'))