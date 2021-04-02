##Dydy2412##
import socket
import threading
import uuid
import pickle

HOST = '127.0.0.1'
PORT = 5555
ADDR = (HOST, PORT)
FORMAT = 'utf-8'

class Server(socket.socket):

    def __init__(self, host:str, port:int, form:int):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

        #Parameter
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.format = form 

        #Setup
        self.bind(ADDR)
        self.listen()
        print(f'[STARTING]: Server host {self.host} is listening on port {self.port}')

        # Storage
        self.clients = []
        self.players = {}
        self.players_ids = self.players.keys()

    def broadcast(self, info, message):
        print(f'[BROADCAST]: ({info}) {message}')
        for client in self.clients:
            paquets = (info , message)
            client.send(pickle.dumps(paquets))

    def kick_all(self):
        for client in self.clients:
            client.close()

    def handle(self, client):
        while True:
            try:
                #Broadcasting Message
                info = pickle.loads(client.recv(2048))  
                if info[0] == 'POS':
                    client_info = info[1]
                    print(f'[MOVING]: {client_info}')
                    self.players[client_info[0]] = client_info[1]
                    self.broadcast('POSS', self.players)

            except:
                #Client Deconnection
                index = self.clients.index(client)
                players_ids_list = list(self.players_ids)
                
                self.clients.remove(client)
                del(self.players[players_ids_list[index]])
                
                self.broadcast('QUIT', players_ids_list[index])
                
                break

    def receive(self):
        while True:
            try:
                # Accept Connection
                client, addr = self.accept()
                print(f'[CLIENT]: Connected with {addr}')

                # Request and Store information
                client_info = pickle.loads(client.recv(2048))

                # Send info of the Server to client
                client.send(pickle.dumps(self.players))

                #Adding player to other machine
                self.broadcast('JOIN', client_info)

                #Update Player list
                self.clients.append(client)
                self.players[client_info[0]] = client_info[1]
                self.broadcast('POSS', self.players)

                # Send to other clients the new Player
                print(f'[CLIENT]: Id is {client_info[0]}')
                client.send(pickle.dumps('Connected to the server!'))

                #Start handleing comunication with client
                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except:
                self.kick_all()
                print('[SERVER]: Server has been terminated...')
                break

if __name__ == "__main__":
    server = Server(HOST, PORT, FORMAT)
    server.receive()
    