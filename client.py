""" Client for SoundConnectPy
    Author: James Parker
    Date: 12th March 2017
"""

import socket

class Client:

    def __init__(self):
        return

    def communicate(self):
        """debug purpose only
        """

        while True:
            message = raw_input("Enter a message to send: ")
            if message == "":
                break
            self.socket.send(message)
        self.socket.close

    def connect(self, host = socket.gethostname()):
        self.socket = socket.socket()
        # just in case a user brutally quits the software
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

        port = 54321

        self.socket.connect((host, port))

    def close(self):
        self.socket.close()

    def send(self, message):
        self.socket.send(message)

if __name__ == '__main__':
    client = Client()
    client.connect()
    client.communicate()
