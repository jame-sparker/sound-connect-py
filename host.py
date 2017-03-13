""" Host for SoundConnectPy
    Author: James Parker
    Date: 12th March 2017
"""
import threading
import socket
import music
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
        print "players info"
        print addr
        print FoxDotHandler.players.keys()
        if addr in FoxDotHandler.players:
            print "prevous player"
            FoxDotHandler.players[addr] >> note
        else:
            print "new player"
            player = Player()
            print note
            player >> note
            FoxDotHandler.players[addr] = player
          
    @staticmethod  
    def removePlayer(addr):
        FoxDotHandler.players[addr].stop()
        del FoxDotHandler.players[addr] 

    @staticmethod
    def update():
        p1 >> pluck([0,2,4], dur=[1,1/2,1/2], amp=[1, 3/4, 3/4])


    @staticmethod
    def stop():
        Clock.stop()

    @staticmethod
    def reset():
        FoxDotHandler.stop()
        FoxDotHandler.players = {}

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

            print received_message

            FoxDotHandler.set_note(self.addr, self.noteFactory(received_message))

        print "Closing"

        FoxDotHandler.removePlayer(self.addr)
        FoxDotHandler.decrement_counter()
        self.client.close()


    def noteFactory(self,message):
        note_text, instrument_text, timing_text = message.split("|")

        instrument_index = music.instrument_names.index(instrument_text)
        print instrument_index
        print instrument_text

        if instrument_index >= 4 and instrument_index <= 8:
            # drum kit

            #not implemented yet
            if instrument_text == "bass_drum":
                pass
            elif instrument_text == "crash":
                pass
            elif instrument_text == "hi_hat_closed":
                pass
            elif instrument_text == "hi_hat_open":
                pass
            elif instrument_text == "snare_drum":
                pass

            return None

        elif instrument_index != -1:
            timing_list = []            

            for text_num in timing_text.split(","):
                n, d = map(float, text_num.split("/"))
                timing_list.append(n/d)

            # remove duplicates
            timing_list = list(set(timing_list))
            timing_list.sort()

            foxdot_timing_list = []
            foxdot_amp_list = [0] + [1] * len(timing_list)

            for i in range(len(timing_list)):
                diff = 0
                if i == 0:
                    diff = timing_list[i]
                else:
                    diff = timing_list[i] - timing_list[i - 1]
                foxdot_timing_list.append(diff)

            foxdot_timing_list.append(1 - timing_list[-1])
            # end of timing creation

            pitch = music.note_to_number(note_text)

            if instrument_text == "pulse":
                return pulse([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "soprano": # flute does not exist 
                return flute([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "marimba":
                return marimba([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "bass":
                return bass([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "bell":
                return bell([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "ripple":
                return ripple([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "zap":
                return zap([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

        return None

class Host:

    def setup_socket(self, hostname = None):
        self.socket = socket.socket()
        if hostname != None:
            host = hostname
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


