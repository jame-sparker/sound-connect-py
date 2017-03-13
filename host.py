""" Host for SoundConnectPy
    Author: James Parker
    Date: 12th March 2017
"""
import threading
import socket
from FoxDot import *

# note: threading.lock -> acquire & release

class FoxDotHandler:
    counter = 0
    counter_lock = threading.Lock()

    players = {} # (addr) -> player

    @staticmethod
    def increment_counter():
        FoxDotHandler.counter_lock.acquire()
        FoxDotHandler.counter += 1
        FoxDotHandler.counter_lock.release()
        print FoxDotHandler.counter

    @staticmethod
    def decrement_counter():
        FoxDotHandler.counter_lock.acquire()
        FoxDotHandler.counter -= 1
        FoxDotHandler.counter_lock.release()
        print FoxDotHandler.counter

    @staticmethod
    def set_note(addr, note): #music note 
        # dictionary is threadsafe by default
        if addr in FoxDotHandler.players:
            FoxDotHandler.players[addr] >> note
        else:
            player = Player()
            player >> note
            
    def removePlayer(addr):
        FoxDotHandler.players[addr].stop()
        del FoxDotHandler.players[addr] 

    @staticmethod
    def update():
        p1 >> pluck([0,2,4], dur=[1,1/2,1/2], amp=[1, 3/4, 3/4])


    @staticmethod
    def stop():
        return

    @staticmethod
    def getTime():
        return Clock.now()



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

        FoxDotHandler.increment_counter()

        while True:
            received_message = self.client.recv(1024)
            if received_message == "":
                break
            FoxDotHandler.set_note(self.addr, "note")

        print "Closing "

        # FoxDotHandler.removePlayer()
        FoxDotHandler.decrement_counter()
        self.client.close()


class Host:

    def setup_socket(self, hostname = None):
        self.socket = socket.socket()
        if hostname != None:
            host = hostname
            # print host
        else:
            host = socket.gethostname()
            print host

        port = 54321

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))


    def listen(self):

        self.socket.listen(5)
        print("listening")
        while True:
            client, addr = self.socket.accept()

            t = Receiver(args=(client,addr,))
            t.start()


if __name__ == '__main__':
    host = Host()
    host.setup_socket()
    host.listen()


