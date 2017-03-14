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
    measures = 4
    counter_lock = threading.Lock()
    measures_lock = threading.Lock()

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
    def increment_measure():
        FoxDotHandler.measures_lock.acquire()
        FoxDotHandler.measures += 1
        FoxDotHandler.measures_lock.release()

    @staticmethod
    def decrement_measure():
        FoxDotHandler.measures_lock.acquire()
        FoxDotHandler.measures -= 1
        FoxDotHandler.measures_lock.release()

    @staticmethod
    def get_measure():
        value = 0
        FoxDotHandler.measures_lock.acquire()
        value = FoxDotHandler.measures
        FoxDotHandler.measures_lock.release()
        return value

    @staticmethod
    def set_note(addr, note, input_args): #music note 
        # dictionary is threadsafe by default
        if addr in FoxDotHandler.players:
            print "prevous player"
            player, _, _ = FoxDotHandler.players[addr]
            player.stop()
            player = Player() # needed to swap to drum kit
            player >> note
            FoxDotHandler.players[addr] = (player, note, input_args)
        else:
            print "new player"
            player = Player()
            player >> note
            FoxDotHandler.players[addr] = (player, note, input_args)
          
    @staticmethod  
    def removePlayer(addr):
        if addr in FoxDotHandler.players:
            player, _, _ = FoxDotHandler.players[addr]
            player.stop()
            del FoxDotHandler.players[addr] 

    @staticmethod
    def update():
        p1 >> pluck([0,2,4], dur=[1,1/2,1/2], amp=[1, 3/4, 3/4])


    @staticmethod
    def stop():
        Clock.clear()

    @staticmethod
    def reset():
        FoxDotHandler.stop()
        FoxDotHandler.players = {}

    @staticmethod
    def getTime():
        return Clock.now()

    @staticmethod
    def restart():
        for p, n, _ in FoxDotHandler.players.values():
            print p, n
            p >> n



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

            note, input_args = self.noteFactory(received_message)
            FoxDotHandler.set_note(self.addr, note, input_args)

        print "Closing"

        FoxDotHandler.removePlayer(self.addr)
        FoxDotHandler.decrement_counter()
        self.client.close()


    def noteFactory(self,message):
        note_text, instrument_text, timing_text = message.split("|")

        instrument_index = music.instrument_names.index(instrument_text)

        measures = FoxDotHandler.get_measure()

        timing_list = []

        if instrument_index >= 4 and instrument_index <= 8:
            # drum kit
            # create a string of "." and "x" based on input

            #not implemented yet

            for text_num in timing_text.split(","):
                n, d = map(float, text_num.split("/"))
                float_value = n / d
                if float_value < measures:
                    timing_list.append(int(float_value * 2))

            # remove duplicates
            timing_list = list(set(timing_list))
            timing_list.sort()

            play_string_list = ["."] * measures * 2

            for i in timing_list:
                play_string_list[i] = "x"

            play_string = "".join(play_string_list)

            # drum doesnt need changes
            if instrument_text == "crash":
                play_string = play_string.replace("x", "#")

            elif instrument_text == "hi_hat_closed":
                play_string = play_string.replace("x", "-")

            elif instrument_text == "hi_hat_open":
                play_string = play_string.replace("x", "=")

            elif instrument_text == "snare_drum":
                play_string = play_string.replace("x", "o")

            print play_string

            return play(play_string, amp=[1]), ([float(x) / 2 for x in timing_list], instrument_index, 0)


        elif instrument_index != -1:

            for text_num in timing_text.split(","):
                n, d = map(float, text_num.split("/"))
                float_value = n / d
                if float_value < measures:
                    timing_list.append(float_value)

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

            foxdot_timing_list.append(measures - timing_list[-1])
            # end of timing creation

            pitch = music.note_to_number(note_text)

            note = None

            if instrument_text == "pulse":
                note = pulse([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "flute": # flute does not exist 
                note = soprano([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "marimba":
                note = marimba([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "bass":
                note = bass([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "bell":
                note = bell([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "ripple":
                note = ripple([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

            elif instrument_text == "zap":
                note = zap([pitch], dur = foxdot_timing_list, amp = foxdot_amp_list, sus = [1./2])

        return note, (timing_list, instrument_index, pitch)

class Host:

    def setup_socket(self, hostname = None):
        self.hostname = hostname
        self.socket = socket.socket()
        if hostname != None:
            host = hostname
        else:
            host = socket.gethostname()
            print host

        self.port = 54321

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, self.port))

    def stop(self):
        socket.socket(socket.AF_INET, 
                  socket.SOCK_STREAM).connect( (self.hostname, self.port))
        self.socket.close()

    def listen(self):

        self.socket.listen(5)
        print("listening")
        while True:
            try:
                client, addr = self.socket.accept()

                t = Receiver(args=(client,addr,))
                t.start()
            except: # socket is closed
                break

        print("server closed")


if __name__ == '__main__':
    host = Host()
    host.setup_socket()
    host.listen()


