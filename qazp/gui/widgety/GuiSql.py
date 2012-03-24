'''
Created on Sep 16, 2011

@author: milosz
'''

class Tabela(object):
    '''
    reprezentuje tabele
    '''

    def __init__(self,nazwa,kolumny,punkt_join,etykiety=[]):
        self.punkt_join = punkt_join
        self.nazwa = nazwa
        self.kolumny = kolumny
        self.etykiety = etykiety
        
    def get_polecenie(self,kolumny=[]):
        select_kolumny = '*'
        if kolumny:
            select_kolumny = ''
            for (ki, k) in enumerate(kolumny):
                if k in self.kolumny:
                    if ki == 0:
                        select_kolumny += k
                    elif ki > 0:
                        select_kolumny += ', '+k
        return 'select '+select_kolumny+' from '+self.nazwa+' '+self.nazwa
    
    def get_kol_et(self):
        ''' kolumny i etykiety. przydatne przy konstruowaniu list, tabelek, itd.'''
        return [(unicode(self.nazwa+'.'+ko),unicode(et)) for (ko, et) in zip(self.kolumny,self.etykiety)]
    
    def get_punkt_join(self,id):
        return self.nazwa+'.'+self.punkt_join[id]
    
    def __str__(self):
        return self.nazwa

def polacz_listy(lista_a, lista_b):
    suma_list = lista_a
    for b in lista_b:
        suma_list.append(b)
    return suma_list

def polacz_mapy(mapa_a, mapa_b):
    suma_map = mapa_a
    for (k,v) in mapa_b.iteritems():
        suma_map[k] = v
    return suma_map

class Join(Tabela):
    
    def __init__(self,tab_a,tab_b):
        Tabela.__init__(self,tab_a.nazwa+' join '+tab_b.nazwa, polacz_listy(tab_a.kolumny,tab_b.kolumny),{})
        
    
class GenJoin(object):
    
    mapa_indeksow = {}
    def __init__(self,tabele):
        self.macierz_join = [[None * len(tabele)] * len(tabele)]
        
    def okresl_join(self,tab_a,tab_b):
        a_indeks, b_indeks  = self.mapa_indeksow[tab_a.nazwa], self.mapa_indeksow[tab_b.nazwa] 