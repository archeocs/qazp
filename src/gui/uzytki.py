# uzytki

from PyQt4.QtGui import QApplication
def to_unicode(s,c=""):
    return QApplication.translate(c, s, None,QApplication.UnicodeUTF8)
    
        