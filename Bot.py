import socket
import struct
import threading
import time

class SABot:
    def __init__(self, Username, Password, IP, Port, Commands):
        self.NullByte = struct.pack('B', 0)
        self.BufSize = 4096
        self.InLobby = False
        self.OnlineUsers = {}
        self.OnlineUserMap = {}
        self.RoomList = {}
        self.NewRoomList = []
        self.banned = False
        self.incorrect = False
        self.creds = ""
        self.receivedCreds = ""

        self.NameToIP = {'2DC': 'ballistick5.xgenstudios.com:1138'}

        self.IPToName = {'ballistick5.xgenstudios.com:1138': '2DC'}
        
        self.convCreds = {'0': '20', '1': '25', '2': '30', '3': '35', '4': '40', '5': '55', '6': '60', '7': '75', '8': '100', '9': '250', 
                          '10': '500', '11': '999', '12': '1500', '13': '5000'}
        
        self.ServerIP = IP
        self.ServerPort = Port
        self.BotServer = self.IPToName[ '{}:{}'.format(self.ServerIP, self.ServerPort)]
            
        self.connectToServer(Username, Password, self.ServerIP, self.ServerPort)

    def sendPacket(self, Socket, PacketData, Receive = False):
        Packet = bytes(PacketData, 'utf-8')

        if Socket:
            Socket.send(Packet + self.NullByte)

            if Receive:
                return Socket.recv(self.BufSize).decode('utf-8')
            
    def connectionHandler(self):
        Buffer = b''

        while hasattr(self, 'SocketConn'):
            try:
                Buffer += self.SocketConn.recv(self.BufSize)
            except OSError:
                if hasattr(self, 'SocketConn'):
                    self.SocketConn.shutdown(socket.SHUT_RD)
                    self.SocketConn.close()

            if len(Buffer) == 0:
                print('Disconnected')
                break
            elif Buffer.endswith(self.NullByte):
                Receive = Buffer.split(self.NullByte)
                Buffer = b''

                for Data in Receive:
                    Data = Data.decode('utf-8')
                  
                    if Data.startswith('0g') or Data.startswith('0j'):
                        print('{{Server}}: {}'.format(Data[2:]))
                    elif Data.startswith('093'):
                        print('Secondary login')
                        break
                    elif Data.startswith('0f') or Data.startswith('0e'):
                        Time, Reason = Data[2:].split(';')
                        print('This account has just been banned [Time: {} / Reason: {}]'.format(Time, Reason))
                    elif Data.startswith('0c'):
                        print(Data[2:])
                    elif Data.startswith('0a'):
                        self.receivedCreds = self.convCreds[Data[2:]]
                        self.creds = str(int(self.creds) + int(self.receivedCreds))
                        print("Received " + self.receivedCreds)

    def connectToServer(self, Username, Password, ServerIP, ServerPort):
        try:
           self.SocketConn = socket.create_connection((ServerIP, ServerPort))
        except Exception as Error:
            print(Error)
            return

        Handshake = self.sendPacket(self.SocketConn, '08HxO9TdCC62Nwln1P', True).strip(self.NullByte.decode('utf-8'))

        if Handshake == '08':
            Credentials = '09{};{}'.format(Username, Password)
            RawData = self.sendPacket(self.SocketConn, Credentials, True).split(self.NullByte.decode('utf-8'))

            for Data in RawData:
                if Data.startswith('A'):
                    self.InLobby = True
                    if self.BotServer != "Squaresville":
                        self.sendPacket(self.SocketConn, "0a")
                        self.creds = Data[3 + len(Username):].replace('#', '').split(';')[8]
                        #print(self.creds)
                        if Data[3 + len(Username):].replace('#', '').split(';')[5] == "1":
                          self.labpass = True

                    print('Logged in to {} with {}'.format(self.BotServer, Username))

                    ConnectionThread = threading.Thread(target=self.connectionHandler)
                    ConnectionThread.start()
                    break
                elif Data == '09':
                    self.incorrect = True
                    print('Incorrect password')
                    break
                elif Data == '091':
                    self.banned = True
                    print('Currently banned')
                    break
        else:
            print('Server capacity check failed')
        
if __name__ == '__main__':
    SABot('',  '', '', 1138, True)
