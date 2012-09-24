'''
Created on Sep 22, 2012

@author: milosz
'''

from datetime import time
from dane.gtypy import Punkt
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
        return {1:'punkt GPS',2:'?',3:self.czas(),4:'Anonim',5:'import'}
    
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