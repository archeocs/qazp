# -*- coding: utf-8 -*-

# polaczenie z baza postgresql

from pol import Polaczenie
import psycopg2

class PolPg(Polaczenie):
    
    #p = None
    info='postgis: '
    geom=True
    def __init__(self,baza,usr,pswd,hn='localhost',host_port='5432'):
        Polaczenie.__init__(self,psycopg2.connect(database=baza,host=hn,port=host_port,user=usr,password=pswd))
        self.info+='%s:%s/%s'%(hn,host_port,baza)
        
    def get_con_info(self):
        return self.info