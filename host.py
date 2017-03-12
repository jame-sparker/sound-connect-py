""" Host for SoundConnectPy
    Author: James Parker
    Date: 12th March 2017
"""
import threading
import socket


class Receiver(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.client = args[0]
        self.addr = args[1]
        return

    def run(self):

        print 'Got connection from', self.addr
        while True:
            received_message = self.client.recv(1024)
            if received_message == "":
                break
            print (received_message)

        print "Closing "
        self.client.close()


class Host:

    def setup_socket(self):
        self.socket = socket.socket()
        host = socket.gethostname()
        port = 54321
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))


    def listen(self):

        self.socket.listen(5)

        while True:
            print "accepting new socket"
            client, addr = self.socket.accept()

            t = Receiver(args=(client,addr,))
            t.start()


host = Host()
host.setup_socket()
host.listen()


