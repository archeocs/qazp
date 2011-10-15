# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialogButtonBox,QWidget,QGridLayout,QLabel,QLineEdit,QComboBox,QPushButton
from PyQt4.QtCore import QRect,Qt

class LokalDialogDef(object):
    
    def setupUi2(self,Dialog):
        Dialog.resize(430,347)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(70, 290, 221, 41))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.formLayoutWidget = QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QRect(10, 20, 400, 261))
        self.gridLayout = QGridLayout(self.formLayoutWidget)
        self.gridLayout.setSpacing(10)
        self.label = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label,0,0)
        self.arkusz_ed = QLineEdit(self.formLayoutWidget)
        self.arkusz_ed.setObjectName("arkusz_ed")
        self.gridLayout.addWidget(self.arkusz_ed,0,1)
        self.label_2 = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label_2,1,0)
        self.nrark_ed = QLineEdit(self.formLayoutWidget)
        self.nrark_ed.setObjectName("nrark_ed")
        self.gridLayout.addWidget(self.nrark_ed,1,1)
        self.label_3 = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label_3,2,0)
        self.miasto_cb = QComboBox(self.formLayoutWidget)
        self.miasto_cb.setObjectName("miasto_cb")
        self.gridLayout.addWidget(self.miasto_cb,2,1)
        self.label_4 = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label_4,3,0)
        self.nrmiej_ed = QLineEdit(self.formLayoutWidget)
        self.nrmiej_ed.setObjectName("nrmiej_ed")
        self.gridLayout.addWidget(self.nrmiej_ed,3,1)
        self.label_5 = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label_5,4,0)
        self.gmina_cb = QComboBox(self.formLayoutWidget)
        self.gmina_cb.setObjectName("gmina_cb")
        self.gridLayout.addWidget(self.gmina_cb,4,1)
        self.label_6 = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label_6,5,0)
        self.powiat_cb = QComboBox(self.formLayoutWidget)
        self.powiat_cb.setObjectName("powiat_cb")
        self.gridLayout.addWidget(self.powiat_cb,5,1)
        self.label_7 = QLabel(self.formLayoutWidget)
        self.gridLayout.addWidget(self.label_7,6,0)
        self.woj_cb = QComboBox(self.formLayoutWidget)
        self.woj_cb.setObjectName("woj_cb")
        self.gridLayout.addWidget(self.woj_cb,6,1)
        self.btnZnajdz = QPushButton(self.formLayoutWidget)
        self.gridLayout.addWidget(self.btnZnajdz,1,2)
       # self.label_8 = QLabel(self.formLayoutWidget)
       # self.label_9 = QLabel(self.formLayoutWidget)
        self.retranslateUi(Dialog)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(319, 347)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 290, 221, 41))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 291, 261))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.arkusz_ed = QtGui.QLineEdit(self.formLayoutWidget)
        self.arkusz_ed.setObjectName("arkusz_ed")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.arkusz_ed)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_6)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_7)
        self.nrark_ed = QtGui.QLineEdit(self.formLayoutWidget)
        self.nrark_ed.setObjectName("nrark_ed")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.nrark_ed)
        self.miasto_cb = QtGui.QComboBox(self.formLayoutWidget)
        self.miasto_cb.setObjectName("miasto_cb")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.miasto_cb)
        self.nrmiej_ed = QtGui.QLineEdit(self.formLayoutWidget)
        self.nrmiej_ed.setObjectName("nrmiej_ed")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.nrmiej_ed)
        self.gmina_cb = QtGui.QComboBox(self.formLayoutWidget)
        self.gmina_cb.setObjectName("gmina_cb")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.gmina_cb)
        self.powiat_cb = QtGui.QComboBox(self.formLayoutWidget)
        self.powiat_cb.setObjectName("powiat_cb")
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.powiat_cb)
        self.woj_cb = QtGui.QComboBox(self.formLayoutWidget)
        self.woj_cb.setObjectName("woj_cb")
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.woj_cb)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtGui.QLabel(self.formLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_9)

        self.retranslateUi(Dialog)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Arkusz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Numer na arkuszu", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Miejscowość", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Nr w miejscowości", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Gmina", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Powiat", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Województwo", None, QtGui.QApplication.UnicodeUTF8))
        self.btnZnajdz.setText(QtGui.QApplication.translate("Dialog", "Znajdź", None, QtGui.QApplication.UnicodeUTF8))
       # self.label_9.setText(QtGui.QApplication.translate("Dialog", "lokalizacji", None, QtGui.QApplication.UnicodeUTF8))
