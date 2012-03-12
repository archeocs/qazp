# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slownik_dialog.ui'
#
# Created: Sun May  1 18:58:13 2011
#      by: PyQt4 UI code generator 4.6.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class SlownikDialogDef(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(416, 413)
        Dialog.setMinimumSize(QtCore.QSize(416, 0))
        Dialog.setMaximumSize(QtCore.QSize(416, 10000))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lista = QtGui.QListWidget(Dialog)
        self.lista.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.lista)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dodaj_btn = QtGui.QPushButton(self.widget)
        self.zmien_btn = QtGui.QPushButton(self.widget)
        self.usun_btn = QtGui.QPushButton(self.widget)
        self.horizontalLayout.addWidget(self.dodaj_btn)
        self.horizontalLayout.addWidget(self.zmien_btn)
        self.horizontalLayout.addWidget(self.usun_btn)
        self.verticalLayout_2.addWidget(self.widget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.dodaj_btn.setText(QtGui.QApplication.translate("MainWindow", "Dodaj", None, QtGui.QApplication.UnicodeUTF8))
        self.zmien_btn.setText(QtGui.QApplication.translate("MainWindow", "Zmień", None, QtGui.QApplication.UnicodeUTF8))
        self.usun_btn.setText(QtGui.QApplication.translate("MainWindow", "Usuń", None, QtGui.QApplication.UnicodeUTF8))
        #self.pushButton.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
