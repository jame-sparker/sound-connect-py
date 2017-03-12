""" Host for SoundConnectPy
    Author: James Parker
    Date: 12th March 2017
"""

import socket

class Host:

    def setup_socket(self):
        self.s = socket.socket()
        host = socket.gethostname()
        port = 54321
        self.s.bind((host, port))


    def listen(self):

        self.s.listen(5)

        while True:
            c, addr = self.s.accept()
            print 'Got connection from', addr
            c.send('Thank you for connecting')
            c.close()


host = Host()
host.setup_socket()
host.listen()
