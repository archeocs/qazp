'''
Created on Jul 8, 2011

@author: milosz
'''
# interfejs polaczenia z baza danych

class Polaczenie:

    def get_stanowiska(self,sql):
        pass
        
    def get_kryteria(self):
        pass
        
    def get_arkusze(self):
        pass
        
    def get_nrark(self,a):
        pass
        
    def lokal_info(self,stan):
        pass
        
    def eksp_info(self,stan):
        pass
    
    def obszar_info(self,stan):
        pass
        
    def teren_info(self,stan):
        pass
        
    def polozenie_info(self,stan):
        pass
        
    def wykonaj(self,sql):
        pass
        
    def zatwierdz(self):
        pass
        
    def wycofaj(self):
        pass