# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 385)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 385))
        MainWindow.setMaximumSize(QtCore.QSize(1000, 385))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(820, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(820, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabela = QtGui.QTableWidget(self.groupBox)
        self.tabela.setObjectName("tableWidget")
        self.tabela.setColumnCount(0)
        self.tabela.setRowCount(0)
        self.horizontalLayout.addWidget(self.tabela)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(140, 0))
        self.groupBox_3.setMaximumSize(QtCore.QSize(140, 16777215))
        self.groupBox_3.setObjectName("groupBox_3")
        self.arkusz_lb = QtGui.QLabel(self.groupBox_3)
        self.arkusz_lb.setGeometry(QtCore.QRect(20, 30, 101, 15))
        self.arkusz_lb.setObjectName("label")
        self.arkusz_cb = QtGui.QComboBox(self.groupBox_3)
        self.arkusz_cb.setGeometry(QtCore.QRect(20, 60, 101, 25))
        self.arkusz_cb.setObjectName("comboBox")
        self.nrark_lb = QtGui.QLabel(self.groupBox_3)
        self.nrark_lb.setGeometry(QtCore.QRect(20, 110, 101, 15))
        self.nrark_lb.setObjectName("label_2")
        self.nrark_cb = QtGui.QComboBox(self.groupBox_3)
        self.nrark_cb.setGeometry(QtCore.QRect(20, 140, 101, 25))
        self.nrark_cb.setObjectName("comboBox_2")
        self.filtr_btn = QtGui.QPushButton(self.groupBox_3)
        self.filtr_btn.setGeometry(QtCore.QRect(20, 190, 80, 25))
        self.filtr_btn.setObjectName("pushButton")
        self.info_btn = QtGui.QPushButton(self.groupBox_3)
        self.info_btn.setGeometry(QtCore.QRect(20, 240, 80, 25))
        self.info_btn.setObjectName("pushButton_2")
        self.lokal_btn = QtGui.QPushButton(self.groupBox_3)
        self.lokal_btn.setGeometry(QtCore.QRect(20,290,80,25))
        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.lok_menu = QtGui.QMenu(self.menubar)
        self.klas_menu = QtGui.QMenu(self.menubar)
        self.zest_menu = QtGui.QMenu(self.menubar)
        self.ust_menu = QtGui.QMenu(self.menubar)
        self.pomoc_menu = QtGui.QMenu(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        self.miasta_akcja = QtGui.QAction(MainWindow)
        self.lok_menu.addAction(self.miasta_akcja)
        self.gminy_akcja = QtGui.QAction(MainWindow)
        self.lok_menu.addAction(self.gminy_akcja)
        self.powiaty_akcja = QtGui.QAction(MainWindow)
        self.lok_menu.addAction(self.powiaty_akcja)
        self.wojewod_akcja = QtGui.QAction(MainWindow)
        self.lok_menu.addAction(self.wojewod_akcja)
        
        self.kultury_akcja = QtGui.QAction(MainWindow)
        self.klas_menu.addAction(self.kultury_akcja)
        self.funkcje_akcja = QtGui.QAction(MainWindow)
        self.klas_menu.addAction(self.funkcje_akcja)
        self.epoki_akcja = QtGui.QAction(MainWindow)
        self.klas_menu.addAction(self.epoki_akcja)
        
        self.typdb_ust_menu = QtGui.QMenu(self.ust_menu)
        self.ust_submenu = QtGui.QAction(MainWindow)
        self.ust_submenu.setMenu(self.typdb_ust_menu)
        self.ust_menu.addAction(self.ust_submenu)
        self.typdb_pg = QtGui.QAction(MainWindow)
        self.typdb_ust_menu.addAction(self.typdb_pg)
        self.typdb_spat = QtGui.QAction(MainWindow)
        self.typdb_ust_menu.addAction(self.typdb_spat)
    
        self.menubar.addAction(self.lok_menu.menuAction())
        self.menubar.addAction(self.klas_menu.menuAction())
        self.menubar.addAction(self.zest_menu.menuAction())
        self.menubar.addAction(self.ust_menu.menuAction())
        self.menubar.addAction(self.pomoc_menu.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "QAZP", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Stanowiska", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Kryteria", None, QtGui.QApplication.UnicodeUTF8))
        self.arkusz_lb.setText(QtGui.QApplication.translate("MainWindow", "Arkusz", None, QtGui.QApplication.UnicodeUTF8))
        self.nrark_lb.setText(QtGui.QApplication.translate("MainWindow", "Nr na arkuszu", None, QtGui.QApplication.UnicodeUTF8))
        self.filtr_btn.setText(QtGui.QApplication.translate("MainWindow", "Filtruj", None, QtGui.QApplication.UnicodeUTF8))
        self.info_btn.setText(QtGui.QApplication.translate("MainWindow", "Szczegóły", None, QtGui.QApplication.UnicodeUTF8))
        self.lokal_btn.setText(QtGui.QApplication.translate("MainWindow", "Lokalizacja", None, QtGui.QApplication.UnicodeUTF8))
        self.lok_menu.setTitle(QtGui.QApplication.translate("MainWindow", "Lokalizacje", None, QtGui.QApplication.UnicodeUTF8))
        self.zest_menu.setTitle(QtGui.QApplication.translate("MainWindow", "Zestawienia", None, QtGui.QApplication.UnicodeUTF8))
        self.miasta_akcja.setText(QtGui.QApplication.translate("MainWindow", "Miejscowości", None, QtGui.QApplication.UnicodeUTF8))
        self.gminy_akcja.setText(QtGui.QApplication.translate("MainWindow", "Gminy", None, QtGui.QApplication.UnicodeUTF8))
        self.powiaty_akcja.setText(QtGui.QApplication.translate("MainWindow", "Powiaty", None, QtGui.QApplication.UnicodeUTF8))
        self.wojewod_akcja.setText(QtGui.QApplication.translate("MainWindow", "Województwa", None, QtGui.QApplication.UnicodeUTF8))
        self.kultury_akcja.setText(QtGui.QApplication.translate("MainWindow", "Kultury", None, QtGui.QApplication.UnicodeUTF8))
        self.funkcje_akcja.setText(QtGui.QApplication.translate("MainWindow", "Funkcje", None, QtGui.QApplication.UnicodeUTF8))
        self.epoki_akcja.setText(QtGui.QApplication.translate("MainWindow", "Epoki", None, QtGui.QApplication.UnicodeUTF8))
        self.klas_menu.setTitle(QtGui.QApplication.translate("MainWindow", "Klasyfikacja", None, QtGui.QApplication.UnicodeUTF8))
        self.ust_menu.setTitle(QtGui.QApplication.translate("MainWindow", "Ustawienia", None, QtGui.QApplication.UnicodeUTF8))
        self.ust_submenu.setText(QtGui.QApplication.translate("MainWindow", "Typ bazy", None, QtGui.QApplication.UnicodeUTF8))
        self.typdb_pg.setText(QtGui.QApplication.translate("MainWindow", "Postgis", None, QtGui.QApplication.UnicodeUTF8))
        self.typdb_spat.setText(QtGui.QApplication.translate("MainWindow", "Spatialite", None, QtGui.QApplication.UnicodeUTF8))
        self.pomoc_menu.setTitle(u'Pomoc')
        #self.actionCcc.setText(QtGui.QApplication.translate("MainWindow", "ccc", None, QtGui.QApplication.UnicodeUTF8))