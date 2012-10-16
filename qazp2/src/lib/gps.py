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

import time
from dane.gtypy import Punkt,Linia
from xml.parsers.expat import ParserCreate

def _czas_pl(st):
    msc = {'STY':'01','LUT':'02','MAR':'03','KWI':'04','MAJ':'05','CZE':'06',
              'LIP':'07','SIE':'08','WRZ':'09','PAZ':'10','LIS':'11','GRU':'12'}
    dt_time = st.strip().split(' ')
    if len(dt_time) != 2 or len(dt_time[0]) != 9:
        return None
    day = dt_time[0][:2]
    mth = msc[dt_time[0][3:6]]
    yr = '20'+dt_time[0][7:]
    tm = dt_time[1]
    if len(tm) == 7:
        tm = '0'+tm
    return '%s-%s-%sT%sZ' % (yr,mth,day,tm)
    
class GpxPunkt(object):
    
    lon,lat,ele = '','',''
    time,name,cmt = '','',''
    desc,type='',''
    dim=2
    _strp_fmt = '%Y-%m-%dT%H:%M:%S'
    
    def __init__(self,lon,lat,atrs={}):
        self.lon = lon
        self.lat = lat
        for (k,v) in atrs.iteritems():
            setattr(self, k, v)
            
    def wkt(self):
        return self.fmt(u'Point(%s %s)')
    
    def fmt(self,f):
        return f % (self.lon,self.lat)
    
    def punkt(self):
        return Punkt(self.lon,self.lat)
    
    def geom(self):
        return self.punkt().geom()
    
    def mapa(self):
        return {1:self.name,2:'?',3:self.czas(),4:'Anonim',5:'import'}
    
    def spr_czas(self):
        if self.time == '':
            tmp = None
            if self.cmt != '':
                tmp = _czas_pl(self.cmt)
            if not tmp and self.desc != '':
                tmp = _czas_pl(self.desc)
            if tmp:
                self.time = tmp
            else:
                return False
        return True
    
    def czas(self):
        return self.time.replace('Z','+0100')
    
    def timestamp(self):
        return time.mktime(time.strptime(self.time.replace('Z',''),self._strp_fmt))
    
class GpxPunktyLista(object):
    
    def __init__(self,lista_pt=[]):
        self.punkty = []
        self.punkty.extend(lista_pt)
        
    def dodaj_punkt(self,gpt):
        self.punkty.append(gpt)
    
    def zlicz(self):
        return len(self.punkty)
    
    def pt_list(self):
        return Linia([Punkt(p.lon,p.lat) for p in self.punkty])
    
    def geom(self):
        return self.pt_list().geom()
    
    def pierw(self):
        return self.punkty[0]
    
    def ost(self):
        return self.punkty[-1]
    
    def min_czas(self):
        return min(self.punkty,key=lambda x: x.time).time
    
    def max_czas(self):
        return max(self.punkty,key=lambda x: x.time).time
    
    def czas_delty(self):
        t = self.punkty[0].timestamp()
        delty = []
        for p in self.punkty[1:]:
            delty.append(abs(t-p.timestamp()))
            t = p.timestamp()
        return delty
    
    def __add__(self,pts):
        if isinstance(pts, GpxPunktyLista):
            return GpxPunktyLista(self.punkty+pts.punkty)

def distr(values):
    m = sum(values) / len(values)
    s = pow(sum([pow(v-m, 2) for v in values]) / len(values), 0.5)
    return (m,s)

class WayPoints(object):
     
    chname,chval = None,''
    cur_pt = None
    def __init__(self):
        self.pts_list = []
        
    def elem_start(self,name,atrs):
        if name == 'wpt':
            self.cur_pt = GpxPunkt(lon=atrs['lon'],lat=atrs['lat'])
        elif not self.chname and not self.chval and self.cur_pt:
            self.chname = name
            self.chval = ''
    
    def tekst(self,txt):
        if self.chname and self.cur_pt:
            self.chval += txt
            
    def elem_end(self,name):
        if name == 'wpt' and self.cur_pt:
            if not self.cur_pt.spr_czas():
                print 'Nieprawidlowy czas'
            self.pts_list.append(self.cur_pt)
            self.chname=None
            self.chval=None
            self.cur_pt=None
        elif self.chname and self.chval and self.cur_pt:
            setattr(self.cur_pt, self.chname, self.chval)
            self.chname = None
            self.chval = None
            
    def create(self,fn):
        parser = ParserCreate()
        parser.StartElementHandler = self.elem_start
        parser.EndElementHandler = self.elem_end
        parser.CharacterDataHandler = self.tekst
        parser.ParseFile(open(fn,'r'))
        
class TrackPoints(object):
    
    def  __init__(self):
        self.segments = []
        self.chname,self.chval = None,''
        self.track = False
        self.cur_seg, self.cur_pt = None,None
    
    def elem_start(self,name,atrs):
        if name == 'trk':
            self.track = True
        elif name == 'trkseg' and self.track and not self.cur_seg:
            self.cur_seg = GpxPunktyLista()
        elif name == 'trkpt' and self.cur_seg and not self.cur_pt:
            self.cur_pt = GpxPunkt(lon=atrs['lon'],lat=atrs['lat'])
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
            self.cur_seg.dodaj_punkt(self.cur_pt)
            self.cur_pt = None
            self.chname = None
            self.chval = None
        elif name == 'trkseg' and self.cur_seg and not self.cur_pt:
            if self.cur_seg.zlicz() > 1:
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
                new_list.extend(self.segments[i].punkty)
        else:
            for s in self.segments:
                new_list.extend(s.punkty)
        return GpxPunktyLista(new_list)
    
    def get_segments(self):
        return self.segments
            
    def create(self,fn):
        parser = ParserCreate()
        parser.StartElementHandler = self.elem_start
        parser.EndElementHandler = self.elem_end
        parser.CharacterDataHandler = self.chdata
        parser.ParseFile(open(fn,'r'))