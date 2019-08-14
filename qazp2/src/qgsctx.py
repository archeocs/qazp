# Copyright (C) 2013 Milosz Piglas <milosz@archeocs.com>
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name ``Milosz Piglas'' nor the name of any other
#    contributor may be used to endorse or promote products derived
#    from this software without specific prior written permission.
# 
# qgsenv IS PROVIDED BY Milosz Piglas ``AS IS'' AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL Milosz Piglas OR ANY OTHER CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from qgis.core import *
from qgis.gui import QgisInterface
from PyQt5.QtCore import pyqtSignal, QObject
import os
__all__ = ['liteUri', 'addVectorLayer', 'vectorLayer', 'initProviders', 'Iface']

def liteUri(db, table, geometryColumn):
    """
    generates QgsDataSourceURI for Spatialite
    """
    src = QgsDataSourceUri()
    src.setDatabase(db)
    src.setDataSource('', table, geometryColumn)
    return src

def vectorLayer(uri, provider, name=None):
    """
    initialize new vector layer from given uri
    """
    testprov = QgsProviderRegistry.instance().library(provider)
    if not testprov:
        raise Exception('Provider ['+provider+'] unknown')
    vn = uri.table()
    if name:
        vn = name
    return QgsVectorLayer(uri.uri(), vn, provider)

def addVectorLayer(uri, provider, name=None):
    """
    initalize new vector layer and adds it to QgsMapLayerRegistry
    """
    lay = vectorLayer (uri, provider, name)
    QgsProject.instance().addMapLayer(lay)
    return lay

def initProviders(libdir=None):
    """
    initialize QgsProviderRegistry from plugins path. 

    - libdir : directory with qgisplugins. If libdir == None it try to
    use path from system variable QGS_PLUGIN
    """
    if libdir:
        QgsProviderRegistry.instance(libdir) #('/usr/lib/qgis/plugins/')
    elif 'QGS_PLUGINS' in os.environ:
        QgsProviderRegistry.instance(os.environ['QGS_PLUGINS'])


class Iface(QgisInterface, QObject):
    """
    simple implementation of QgisInterface, which might be usefull in some
    cases
    """
    def __init__(self):
        QgisInterface.__init__(self)
        QObject.__init__(self)
        self._active = None
        self.initializationCompleted.emit()
    
    def addVectorLayer(self, path, name, provider):
        return addVectorLayer(path, provider, name)

    def setActiveLayer(self, layer):
        if not layer:
            self._active = None
            return True
        test = QgsProject.instance().mapLayer(layer.id())
        if test:
            self._active = layer
            self.currentLayerChanged.emit()
            return True
        return False

    def activeLayer(self):
        return self._active

    currentLayerChanged = pyqtSignal(QgsMapLayer, name='currentLayerChanged')

    initializationCompleted = pyqtSignal(name='initializationCompleted')
        
initProviders('/usr/lib/qgis/plugins/')