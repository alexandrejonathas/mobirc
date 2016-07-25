import asyncio
import socket
import ast

from client_manager import ClientManager
import server_config as config


class Server(object):

    def __init__(self, loop, host, port):
        self.loop = loop
        self._serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._serv_sock.setblocking(0)
        self._serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._serv_sock.bind((host,port))
        self._serv_sock.listen(5)
        self.__clients = []
        asyncio.Task(self._server())
        print('Server is open {}:{}'.format(host, port))

    @property
    def clients(self):
        '''
            Retorna uma lista de clientes
        '''
        return self.__clients

    def remove(self, client):
        self.__clients.remove(client)
        self.broadcast(to='all', message='Client {} quit!\n'.format(client.addr))

    def broadcast(self, to, message):
        '''
            Metódo que delega para o cliente o envio das msg.
        '''
        for client in self.__clients:
            if to == 'all':
                client.send(message)
            else:
                if to == client.nick:
                    client.send(message)


    @asyncio.coroutine
    def _server(self):
        '''
            Aceita as conexões e adiciona a uma lista de clientes
        '''
        while True:
            conn, addr = yield from self.loop.sock_accept(self._serv_sock)
            conn.setblocking(0)
            client = ClientManager(self, conn, addr)
            self.__clients.append(client)
            #self.broadcast(message='Client {} connected!\n'.format(client.addr))

def main():
    loop = asyncio.get_event_loop()
    Server(loop, config.address['host'], config.address['port'])
    loop.run_forever()

if __name__ == '__main__':
    main()
