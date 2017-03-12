""" Client for SoundConnectPy
    Author: James Parker
    Date: 12th March 2017
"""

import socket

s = socket.socket()
host = socket.gethostname()
port = 54321

s.connect((host, port))
print s.recv(1024)
s.close