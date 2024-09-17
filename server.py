import socket
import threading
import uuid
import random
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.started = False
        self.game = {}

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen()

        while True:
            socket, address = self.server.accept()
            first = None

            playerInfo = b''
            while True:
                buff = socket.recv(1024)
                playerInfo += buff
                if len(buff) < 1024:
                    break

            playerInfo = json.loads(playerInfo.decode())
            if len(self.game) == 0:
                colour = random.choice(["White", "Black"])
                self.game[playerInfo["id"]] = {"ready": False, "colour": colour, "pieces": playerInfo["pieces"], "taken": playerInfo["taken"], "state": playerInfo["state"]}
                if colour == "White":
                    first = playerInfo["id"]
            else:
                colour = ""
                for value in self.game.values():
                    if not isinstance(value, str):
                        if value["colour"] == "White":
                            colour = "Black"
                        else:
                            colour = "White"
                            first = playerInfo["id"]
                
                self.game[playerInfo["id"]] = {"ready": False, "colour": colour, "pieces": playerInfo["pieces"], "taken": playerInfo["taken"], "state": playerInfo["state"]}
            
            if first != None:     
                self.game["turn"] = first

            socket.send('received'.encode())

            thread = threading.Thread(target=self.handleClient, args=(socket, address, playerInfo["id"]))
            thread.start()

    def handleClient(self, conn, address, userId):
        connected = True

        while connected:
            connectedPlayers = 0
            if not self.game:
                connected = False
                continue
            
            for value in self.game.values():
                if not isinstance(value, str):
                    if value["ready"]:
                        connectedPlayers += 1

            try:
                data = conn.recv(4096).decode('utf-8')
                data = json.loads(data)

                if not self.started:
                    conn.send(json.dumps({"started": self.started, "connections": connectedPlayers, "players": len([k for k in list(self.game.keys()) if k != "turn"])}).encode('utf-8'))
                else:
                    if "ready" not in data.keys():
                        if data["moved"] and userId == self.game["turn"]:
                            self.game["turn"] = [id for id in list(self.game.keys()) if id != userId and id != "turn"][0]

                        otherId = [id for id in list(self.game.keys()) if id != userId and id != "turn"][0]
                    
                    dataToSend = {"started": True, "players": {}}
                    for key, value in self.game.items():
                        if "ready" not in data.keys():
                            self.game[userId]["colour"] = data["colour"]
                            self.game[userId]["pieces"] = data["pieces"]
                            self.game[userId]["taken"] = data["taken"]
                            self.game[userId]["state"] = data["state"]
                        dataToSend["players"][key] = value
                    if "turn" in self.game.keys():
                        dataToSend["turn"] = self.game["turn"]
                    conn.sendall(json.dumps(dataToSend).encode('utf-8'))
            except ConnectionResetError:
                connected = False
                continue
            except IndexError:
                conn.sendall(json.dumps({"disconnect": True}).encode('utf-8'))
                connected = False
                continue

            if data["disconnect"] == True:
                connected = False
                continue

            if not self.started:
                if "ready" in data.keys():
                    if data["ready"] == True:
                        if not self.game[userId]["ready"]:
                            self.game[userId]["ready"] = True
                            connectedPlayers += 1
                            if connectedPlayers == 2:
                                self.started = True

        self.game = {}
        self.started = False
        conn.close()
        print("Connection Closed")

host = socket.gethostbyname(socket.gethostname())
port = 9999

server = Server(host, port)
server.start()
