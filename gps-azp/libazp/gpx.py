'''
Created on Mar 14, 2012

@author: milosz
'''

#from xml.dom.minidom import parse
from xml.parsers.expat import ParserCreate
from geom import Line
from functools import partial


class TrackList(object):
    
    seg,pt,time=False,False,False
    itime,xtime='','' # min time, maxtime
    geo_line = None
    def __init__(self):
        self.tracks = [] # Line, min_time, max_time
        self.parser = ParserCreate()
    
    def start_element(self,name,atrs):
        if name == 'trkseg':
            self.seg = True
            self.geo_line = Line()
        elif name == 'trkpt':
            self.pt = True
            self.geo_line.add_point((atrs['lon'],atrs['lat']))
        elif name == 'time':
            self.time = True
            
    def end_element(self,name):
        if name == 'trkseg':
            self.seg = False
            self.pt = False
            self.time = False
            if self.geo_line.count_pts() > 1:
                self.tracks.append((self.geo_line,self.itime,self.xtime,self.geo_line.count_pts()))
            self.geo_line = None
            self.itime = ''
            self.xtime = ''
        elif name == 'trkpt':
            self.pt = False
            self.time = False
        elif name == 'time':
            self.time = False
            
    def char_data(self,txt):
        if self.time and len(txt) >= 19:
            if txt > self.xtime:
                self.xtime = txt
            if self.itime == '' or txt < self.itime:
                self.itime = txt
                
    def get_list(self,fn):
        self.parser.StartElementHandler = self.start_element 
        self.parser.EndElementHandler = self.end_element
        self.parser.CharacterDataHandler = self.char_data
        self.parser.ParseFile(open(fn,'r'))
        return self.tracks

class Track(object):
    
    # czy poszczegolne segmenty (rozniace sie czasem dodania) wprowadzac jako osobne linie???
    
    pt_element=False
    time_element=False
    min_time,max_time = '',''
    def __init__(self):
        self.parser = ParserCreate()
        #self.parser.StartElementHandler = self.track_point
    
    def start_point(self,nazwa,atrybuty,line):
        if nazwa == 'trkpt':
            self.pt_element = True
            line.add_point((atrybuty['lon'],atrybuty['lat']))
        elif nazwa == 'time':
            self.time_element = True
    
    def end_point(self,nazwa):
        if nazwa == 'trkpt':
            self.pt_element = False
        elif nazwa == 'time':
            self.time_element = False
                
    def char_data(self,txt):
        if self.pt_element and self.time_element:
            #print txt, self.min_time, self.max_time
            if self.min_time == '':
                self.min_time = txt
            if len(txt) == 20 and self.max_time < txt:
                self.max_time = txt
                    
    def get_line(self,file_name):
        line = Line()
        self.parser.StartElementHandler = partial(self.start_point,line=line) 
        self.parser.EndElementHandler = self.end_point
        self.parser.CharacterDataHandler = self.char_data
        self.parser.ParseFile(open(file_name,'r'))
        return line
        
    def get_time(self,tz="+0100"):
      #  strp_fmt = '%Y-%m-%dT%H:%M:%S%z'
        nt = self.min_time
        xt = self.max_time
        if len(nt) == 20 and nt.endswith('Z'):
            nt = nt.replace('Z',tz)
        elif len(nt) == 19:
            nt += tz
        elif len(nt) != 24:
            print 'nieprawidlowy format '+nt
        if len(xt) == 20 and xt.endswith('Z'):
            xt = xt.replace('Z',tz)
        elif len(xt) == 19:
            xt += tz
        elif len(xt) != 24:
            print 'nieprawidlowy format '+xt    
        return (nt,xt)