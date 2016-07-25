# -*- coding: utf-8 -*-
import sys

import asyncio
import socket

import client_config as config

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from client_controller import ClientController

from chat import Chat

form_class = uic.loadUiType('connect.ui')[0]

class Connect(QtWidgets.QDialog, form_class):
    def __init__(self, controller, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        #loadUi('mainwindow.ui', self)

        self.__controller = controller

        self.setupUi(self)

        self.btOK.clicked.connect(self.btOK_clicked)

    def btOK_clicked(self):
        self.__controller._sock.send(str({'nick': self.txtNick.text()}).encode('utf-8'))
        self.inicializaChat()

    def inicializaChat(self):
        chat = Chat(self.__controller)
        chat.show()
        self.close()
        chat.exec()



loop = asyncio.get_event_loop()
controller = ClientController(loop, config.address['host'], config.address['port'])

app = QtWidgets.QApplication(sys.argv)
connect = Connect(controller)
connect.show()
app.exec_()

loop.run_forever()
