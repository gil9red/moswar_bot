# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Sep 10 17:43:50 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(847, 573)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.url_le = QtGui.QLineEdit(self.centralwidget)
        self.url_le.setReadOnly(True)
        self.url_le.setObjectName("url_le")
        self.horizontalLayout_2.addWidget(self.url_le)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commands_cb = QtGui.QComboBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commands_cb.sizePolicy().hasHeightForWidth())
        self.commands_cb.setSizePolicy(sizePolicy)
        self.commands_cb.setObjectName("commands_cb")
        self.horizontalLayout.addWidget(self.commands_cb)
        self.run_pb = QtGui.QPushButton(self.centralwidget)
        self.run_pb.setObjectName("run_pb")
        self.horizontalLayout.addWidget(self.run_pb)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.view = QtWebKit.QWebView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view.sizePolicy().hasHeightForWidth())
        self.view.setSizePolicy(sizePolicy)
        self.view.setProperty("url", QtCore.QUrl("about:blank"))
        self.view.setObjectName("view")
        self.verticalLayout.addWidget(self.view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dock_widget_exec = QtGui.QDockWidget(MainWindow)
        self.dock_widget_exec.setObjectName("dock_widget_exec")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_exec = QtGui.QPushButton(self.dockWidgetContents_2)
        self.button_exec.setObjectName("button_exec")
        self.verticalLayout_2.addWidget(self.button_exec)
        self.code = QtGui.QPlainTextEdit(self.dockWidgetContents_2)
        self.code.setObjectName("code")
        self.verticalLayout_2.addWidget(self.code)
        self.dock_widget_exec.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_widget_exec)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Бот moswar\'а", None, QtGui.QApplication.UnicodeUTF8))
        self.run_pb.setText(QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))
        self.dock_widget_exec.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Выполнение скрипта", None, QtGui.QApplication.UnicodeUTF8))
        self.button_exec.setText(QtGui.QApplication.translate("MainWindow", "Выполнить", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
