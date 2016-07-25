#-*- coding: utf-8 -*-
from threading import Thread
import socket
import ast
import client_config as config

class ClientController(object):

    def __init__(self, loop, host, port):
        self.__loop = loop
        self.__cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__cli_sock.connect((host,port))
        self.__messages = []
        #asyncio.Task(self.message_handler())

    @property
    def _sock(self):
        return self.__cli_sock

    def send(self, to, message):
        message = {'to': to, 'message': message}
        self._sock.send(str(message).encode('utf-8'))
