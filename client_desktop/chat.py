# -*- coding: utf-8 -*-

import sys
from threading import Thread

from PyQt5 import QtWidgets, uic

from client_controller import ClientController

import client_config as config

import ast

import os
form_class = uic.loadUiType(os.path.join(config.TEMPLATE_DIR, 'chat.ui'))[0]

class Chat(QtWidgets.QDialog, form_class):
    def __init__(self, controller, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.__controller = controller
        self.__client_selected = 'all'

        self.setupUi(self)

        self.btSend.clicked.connect(self.send)

        self.lvClients.itemClicked.connect(self.item_selected)

        self.start_thread()

    def start_thread(self):
        t = Thread(target=self.message_handler)
        t.start()

    def send(self):
        self.__controller.send(to=self.__client_selected, message=self.txtMessage.text())
        self.txtMessage.setText('')

    def item_selected(self, item):
        print(item.text())
        self.__client_selected = item.text()

    def message_handler(self):
        '''
            Fica escutando as mensagens
        '''
        while True:
            buf = self.__controller._sock.recv(config.MESSAGE_BUFFER)
            if buf == b'':
                self.__update = False
                break

            message = ast.literal_eval(buf.decode('utf8'))

            self.lvClients.clear()

            item = QtWidgets.QListWidgetItem('all')
            self.lvClients.addItem(item)

            for client in message['clients']:
                item = QtWidgets.QListWidgetItem(client)
                self.lvClients.addItem(item)

            if message['message']:
                message = QtWidgets.QListWidgetItem(message['message'])
                self.lvMessages.addItem(message)
