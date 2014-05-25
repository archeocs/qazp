# -*- coding: utf-8 -*-

# (c) Milosz Piglas 2014 Wszystkie prawa zastrzezone

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

from PyQt4 import QtCore as core
from PyQt4 import QtGui as gui
from pyqube import pyqube as p
from pyqube import views as v
from functools import partial

class Matrix(object):

    def __init__(self):
        self._labels = [u'Attribute', u'Alias', u'Sort', u'Visible', u'Function', u'Condition', u'Or']
        self._labelsCount = len(self._labels)
        self._columns = {}
        self._columnCount = 5
        self._rowCount = 7
        
    def label(self, row):
        if row < self._labelsCount:
            return self._labels[row]
        return self._labels[-1]
    
    def setValue(self, index, value):
        r, c = index.row(), index.column()
        column = self._columns.get(c, {})
        column[r] = value
        self._columns[c] = column
        if r >= self._rowCount-1:
            self._rowCount += 1
        if c >= self._columnCount-1:
            self._columnCount  += 1
            
    def value(self, index):
        r, c = index.row(), index.column()
        return self.cellValue(r, c)
    
    def cellValue(self, r, c):
        column = self._columns.get(c, {})
        if r == 2:
            return column.get(r, False)
        elif r == 3:
            return column.get(r, True)
        else:
            return column.get(r, None)
    
    @property
    def rowCount(self):
        return self._rowCount
    
    @property    
    def columnCount(self):
        return self._columnCount     

class ValueConverter(object):

    def fromInput(self, text):
        return text
        
    def toOutput(self, value):
        return value
        
class AttrConverter(ValueConverter):

    def __init__(self, schema):
        ValueConverter.__init__(self)
        self.schema = schema
        
    def fromInput(self, text):
        return self.schema.attrByName(unicode(text))
        
    def toOutput(self, value):
        if value and isinstance(value, v.ViewAttr):
            return value.fullName()    
        elif value:
            return value
        else:
            return None
            
class AttrValidator(gui.QValidator):
    
    def __init__(self, schema, parent=None):
        gui.QValidator.__init__(self, parent=parent)
        self.schema = schema
        self.viewAttrs = []
        
    def validate(self, qtext, pos):
        text = unicode(qtext)
        if not text:
            return (gui.QValidator.Intermediate, pos)
        elif '.' in text:
            if not self.viewAttrs:
                v =  self.schema.viewByName(text[:text.index('.')])
                if not v:
                    return (gui.QValidator.Invalid, pos)
                else:
                    self.viewAttrs = [a.realName() for a in v.viewAttrs()]
            elif len(text) > text.index('.')+1:
                attr = text[text.index('.')+1:]
                for a in self.viewAttrs:
                    if a == attr:
                        return (gui.QValidator.Acceptable, pos)
                    elif a.startswith(attr):
                        return (gui.QValidator.Intermediate, pos)
        return (gui.QValidator.Intermediate, pos)
        
        
        
class BoolConverter(ValueConverter):
    
    def __init__(self):
        ValueConverter.__init__(self)
        
    def fromInput(self, variant):
        return variant.toBool()
        
    def toOutput(self, value):
        return value
        
class StrConverter(ValueConverter):
    
    def __init__(self):
        ValueConverter.__init__(self)
        
    def fromInput(self, variant):
        if isinstance(variant, core.QVariant):
            return unicode(variant.toString())
        elif isinstance(variant, core.QString):
            return unicode(variant)
        
    def toOutput(self, value):
        return value 

class EditorTableModel(core.QAbstractTableModel):

    def __init__(self, schema, matrix ):
        core.QAbstractTableModel.__init__(self)
        self.schema = schema
        self.matrix = matrix
        strc = StrConverter()
        boolc = BoolConverter()
        self.converters = {0:AttrConverter(self.schema), 1:strc, 2:boolc, 3:boolc, 4:strc, 5:strc, 6:strc }
    
    def _converter(self, row):
        if row < 7:
            return self.converters[row]
        else:
            return self.converters[6]
    
    def flags(self,indeks):
        return core.Qt.ItemIsEnabled | core.Qt.ItemIsEditable | core.Qt.ItemIsSelectable
        
    def headerData(self, section, orientation, role):
        if orientation == core.Qt.Vertical and role == core.Qt.DisplayRole:
            return self.matrix.label(section)
        elif orientation == core.Qt.Horizontal and role==core.Qt.DisplayRole:
            return unicode(section+1)
        else:
            return core.QVariant()
        
    def rowCount(self, model):
        return self.matrix.rowCount
        
    def columnCount(self, model):
        return self.matrix.columnCount
        
    def data(self, index, role=core.Qt.DisplayRole):
        v = self.matrix.value(index)
        if role == core.Qt.DisplayRole:
            return self._converter(index.row()).toOutput(v)
        elif role == core.Qt.EditRole:
            return self._converter(index.row()).toOutput(v)
        return core.QVariant()

    def setData(self, index, value, role=core.Qt.EditRole):
        self.beginResetModel()
        self.matrix.setValue(index, self._converter(index.row()).fromInput(value))
        self.endResetModel()
        self.dataChanged.emit(index, index)
        return True

class AttributesDelegate(gui.QStyledItemDelegate):

    def __init__(self, schema, tableView):
        gui.QStyledItemDelegate.__init__(self, parent=tableView)
        self.setItemEditorFactory(gui.QItemEditorFactory.defaultFactory())
        self.schema = schema
        self.matrix = tableView.model().matrix
        
    def _attrs(self, index):
        selected = set([])
        for c in range(self.matrix.columnCount):
            if c == index.column():
                continue
            a = self.matrix.cellValue(0, c)
            if a:
                sv = unicode(a.fullName())
                attr = self.schema.attrByName(sv)
                for view in self.schema.relatedViews(attr.view):
                    selected = selected | set([x.fullName() for x in view.viewAttrs() ])
                selected = selected | set([x.fullName() for x in attr.view.viewAttrs()])
        if selected:
            return list(selected)
        else:
            return [a.fullName() for a in self.schema.attributes()]
        
    def createEditor(self, parent, style, index):
        self.initStyleOption(style, index)
        textField = gui.QLineEdit(parent)
        completer = gui.QCompleter(self._attrs(index))
        completer.setCaseSensitivity(core.Qt.CaseInsensitive)
        textField.setCompleter(completer)
        textField.setValidator(AttrValidator(self.schema, textField))
        textField.acceptableInput=True
        return textField
        
    def setEditorData(self, editor, index):
        value = index.data().toString()
        editor.setText(value)
    
    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        
class ListDelegate(gui.QStyledItemDelegate):

    def __init__(self, values, tableView):
        gui.QStyledItemDelegate.__init__(self, parent=tableView)
        self.setItemEditorFactory(gui.QItemEditorFactory.defaultFactory())
        self.values = values
    
    def createEditor(self, parent, style, index):
        r = index.row()
        if r > 3 and r < 7:
            return self._createLineEditor(parent, style, index, self.values[r])
        elif r >= 7:
            return self._createLineEditor(parent, style, index, self.values[6])
        else:
            return gui.QStyledItemDelegate.createEditor(self, parent, style, index)
            
    def setEditorData(self, editor, index):
        r = index.row()
        if r > 3:
            self._setEditorTextData(editor, index)
        else:
            gui.QStyledItemDelegate.setEditorData(self, editor, index)
            
    def setModelData(self, editor, model, index):
        r = index.row()
        if r > 3:
            self._setModelTextData(editor, model, index)
        else:
            gui.QStyledItemDelegate.setModelData(self, editor, model, index)
        
    def _createLineEditor(self, parent, style, index, valuesList):
        self.initStyleOption(style, index)
        textField = gui.QLineEdit(parent)
        completer = gui.QCompleter(valuesList)
        completer.setCaseSensitivity(core.Qt.CaseInsensitive)
        textField.setCompleter(completer)
        return textField
        
    def _setEditorTextData(self, editor, index):
        value = index.data().toString()
        editor.setText(value)
    
    def _setModelTextData(self, editor, model, index):
        model.setData(index, editor.text())
        
class QtQube(gui.QWidget):
    
    def __init__(self, schema, parent=None):
        gui.QWidget.__init__(self, parent=parent)
        self.setLayout(gui.QVBoxLayout(self))
        self.schema = schema
        tableView = gui.QTableView()
        self.layout().addWidget(tableView)
        self.matrix = Matrix()
        model = EditorTableModel(schema, self.matrix)
        tableView.setModel(model)
        functionNames = ['avg', 'count', 'sum']
        operators = ['<', '<=', '=', '>=', '>', 'LIKE']
        tableView.setItemDelegate(ListDelegate({4:functionNames, 5:operators, 6:operators}, tableView))
        tableView.setItemDelegateForRow(0, AttributesDelegate(schema, tableView))
        #tableView.horizontalHeader().setResizeMode(gui.QHeaderView.Stretch)
    
    def _createConditions(self, column):
        chain = v.ConditionChain()
        size = 0
        andOp = self.matrix.cellValue(5, column)
        if andOp:
            size += 1
            chain.addAnd(andOp)
        for r in range(6, self.matrix.rowCount):
            operator = self.matrix.cellValue(r, column)
            if operator:
                size += 1
                chain.addOr(operator)
        if size > 0:
            return chain.build() 
        else:
            return None
        
    def getQuery(self):
        
        builder = p.QueryBuilder(self.schema)
        selectAttrs = {}
        aggrAttrs = []
        attrCond = {}
        viewHasCond = {}
        for c in range(self.matrix.columnCount):
            attr = self.matrix.cellValue(0, c)
            if attr:
                conditions = self._createConditions(c)
                if conditions:
                    attrCond[c] = conditions
                    if not viewHasCond.get(attr.view.name, False):
                        viewHasCond[attr.view.name] = True
        for c in range(self.matrix.columnCount):
            attr = self.matrix.cellValue(0, c)
            if attr:
                visible = self.matrix.cellValue(3, c)
                sort = self.matrix.cellValue(2, c)
                conditions = attrCond.get(c, None)
                alias = self.matrix.cellValue(1, c)
                fname = self.matrix.cellValue(4, c)
                selectAttrs[c] = attr.select(orderBy=sort, visible=visible, condition=conditions, altName=alias)
                if fname and visible:
                    selectAttrs[c].aggregate = partial(function, fname)
                    aggrAttrs.append(c)
                builder.add(selectAttrs[c], outerJoin=(not viewHasCond.get(attr.view.name, False)) )
        if aggrAttrs:
            for (i, attr) in selectAttrs.iteritems():
                if i not in aggrAttrs and attr.visible:
                    attr.groupBy = True
        return builder.build()

def function(name, attr):
    return name+'('+attr+')'
        
def createSchema():
    booksView = v.View('books', u'Books', ['title', 'author', 'year', 'publisher', 'category'])
    publishersView = v.View('publishers', 'Publishers', ['id', 'name', 'city'])
    categoriesView = v.View('categories', 'Categories', ['id', 'category_name'])
    categoriesView['category_name'].userName = 'Category name'
    citiesView = v.View('cities', 'Cities', ['id', 'city_name'])
    
    bookPublisher = v.Relation(
                            [v.AttrPair
                                (booksView['publisher'], 
                                            publishersView['id']
                                )
                            ]
                            )
    publisherCity = v.Relation(
                            [v.AttrPair
                                (
                                    publishersView['city'], 
                                    citiesView['id']
                                )
                            ]
                            )
    bookCategory = v.Relation(
                           [v.AttrPair
                                (
                                    booksView['category'], 
                                    categoriesView['id']
                                )
                            ]
                            )
    schema = v.Schema()
    schema.addView(booksView)
    schema.addView(publishersView, bookPublisher)
    schema.addView(categoriesView, bookCategory)
    schema.addView(citiesView, publisherCity)
    return schema
        
def main():
    import sys
    app = gui.QApplication(sys.argv)
    dialog = gui.QDialog()
    dialog.setLayout(gui.QVBoxLayout())
    widget = QtQube(createSchema(), dialog)
    dialog.layout().addWidget(widget)
    dialog.setMinimumSize(500, 500)
    dialog.exec_()
    q = widget.getQuery()
    print q.statement
    print q.params
    print q.attributes

if __name__ == '__main__':
    main()
