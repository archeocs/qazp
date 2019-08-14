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

from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QImage
from os.path import basename

def odczyt(ident, con, nout=None):
    stmt = con.prep('select dane from media where id=?')
    w = stmt.jeden([ident])
    if w is None:
        return None
    bajty = QByteArray.fromRawData(w[0])
    return QImage.fromData(bajty)

def zapiszMapa(plik, st, syg, con, format=None):
    mx = con.getMax('media','id')+1
    stmt = con.prep("insert into media(id, sygnatura, plik, format, tabela, dane) values(?, ?, ?, ?, 'S', ?)")
    s2 = con.prep('insert into st_media(medium, stanowisko,typ) values(?,?,?)')
    img = QImage(plik)
    buf = QBuffer()
    buf.open(QIODevice.WriteOnly)
    if img.save(buf, format):
        if stmt.wykonaj([mx, syg, basename(plik), format, memoryview(buf.buffer().data())], False) != 1:
            con.wycofaj()
            return False
        if s2.wykonaj([mx,st,'M'],False) != 1:
            con.wycofaj()
            return False
        return True
    return False

def usunMapa(st, ident, con):
    ps = con.prep('delete from st_media where stanowisko=? and medium=? and typ=?')
    if ps.wykonaj([st, ident, 'M']) != 1:
        con.wycofaj()
        return False
    ps = con.prep('delete from media where id=? and tabela=?')
    if ps.wykonaj([ident, 'S']) != 1:
        con.wycofaj()
        return False
    return True