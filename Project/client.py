import socket
import json

class Client:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 9999
        self.connected = False
        self.ready = False

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, player):
        if not self.connected:
            try:
                self.client.connect((self.host, self.port))
            except Exception:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((self.host, self.port))
            self.connected = True
            data = json.dumps({"id": str(player.userId), "pieces": [], "taken": [], "state": ""})
            self.send(data)

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.ready = False
            self.client.close()
    
    def send(self, msg):
        self.client.send(msg.encode('utf-8'))

    def receive(self):
        msg = self.client.recv(4096)
        return msg.decode()
