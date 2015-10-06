# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Tue Oct  6 20:22:33 2015
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
        self.menuDockWindow = QtGui.QMenu(self.menubar)
        self.menuDockWindow.setObjectName("menuDockWindow")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
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
        self.dock_widget_simple_log = QtGui.QDockWidget(MainWindow)
        self.dock_widget_simple_log.setObjectName("dock_widget_simple_log")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setContentsMargins(-1, 3, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.clear_slog = QtGui.QToolButton(self.dockWidgetContents)
        self.clear_slog.setObjectName("clear_slog")
        self.verticalLayout_3.addWidget(self.clear_slog)
        self.simple_log = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.simple_log.setObjectName("simple_log")
        self.verticalLayout_3.addWidget(self.simple_log)
        self.dock_widget_simple_log.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_widget_simple_log)
        self.toolBarGeneral = QtGui.QToolBar(MainWindow)
        self.toolBarGeneral.setObjectName("toolBarGeneral")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarGeneral)
        self.actionStartTimer = QtGui.QAction(MainWindow)
        self.actionStartTimer.setObjectName("actionStartTimer")
        self.actionStopTimer = QtGui.QAction(MainWindow)
        self.actionStopTimer.setObjectName("actionStopTimer")
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBarGeneral.addAction(self.actionStartTimer)
        self.toolBarGeneral.addAction(self.actionStopTimer)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.clear_slog, QtCore.SIGNAL("clicked()"), self.simple_log.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Бот moswar\'а", None, QtGui.QApplication.UnicodeUTF8))
        self.run_pb.setText(QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDockWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Окна", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.dock_widget_exec.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Выполнение скрипта", None, QtGui.QApplication.UnicodeUTF8))
        self.button_exec.setText(QtGui.QApplication.translate("MainWindow", "Выполнить", None, QtGui.QApplication.UnicodeUTF8))
        self.dock_widget_simple_log.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Простой лог", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_slog.setToolTip(QtGui.QApplication.translate("MainWindow", "Очистить лог", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_slog.setStatusTip(QtGui.QApplication.translate("MainWindow", "Очистить лог", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_slog.setText(QtGui.QApplication.translate("MainWindow", "Очистить лог", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarGeneral.setWindowTitle(QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStartTimer.setText(QtGui.QApplication.translate("MainWindow", "Start Timer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStartTimer.setToolTip(QtGui.QApplication.translate("MainWindow", "Start Timer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStopTimer.setText(QtGui.QApplication.translate("MainWindow", "Stop Timer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStopTimer.setToolTip(QtGui.QApplication.translate("MainWindow", "Stop Timer", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
