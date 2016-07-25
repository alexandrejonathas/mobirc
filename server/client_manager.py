import asyncio
import ast
import server_config as config

class ClientManager(object):
    def __init__(self, server, conn, addr):
        self.addr = addr
        self.__conn = conn
        self.__server = server
        self.__nick = None
        asyncio.Task(self.client_handler())

    @property
    def nick(self):
        return self.__nick

    def send(self, data):
        return self.__server.loop.sock_sendall(self.__conn, data.encode('utf8'))

    @asyncio.coroutine
    def client_handler(self):
        '''
            Starta o metodo que fica escutando as mensagens dos clientes,
            se ocorrer algum erro na comunicação ele remove o cliente
        '''
        try:
            yield from self.client_loop()
        except IOError:
            pass
        finally:
            self.__server.remove(self)

    @asyncio.coroutine
    def client_loop(self):
        '''
            Fica escutando as mensagens
        '''
        while True:
            buf = yield from self.__server.loop.sock_recv(self.__conn, config.MESSAGE_BUFFER)
            if buf == b'':
                break

            dicionario = ast.literal_eval(buf.decode('utf8'))

            to = 'all'

            if self.__nick is None:
                self.__nick = dicionario['nick']
                message = message='{} entered the chat'.format(self.__nick)
            else:
                to = dicionario['to']
                message = 'From {} to {}: {}'.format(self.__nick, to, dicionario['message'])

            self.__server.broadcast(to=to, message=message)
