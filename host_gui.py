import sys
import os
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import host
import time

class HostWidget(QWidget):
    def __init__(self, parent=None):
        super(HostWidget, self).__init__(parent)

        self.host = host.Host()

        # set background color

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
        main_vbox = QVBoxLayout()
        main_vbox.setMargin(50)
        main_vbox.addStretch() ## temporary

        control_hbox = QHBoxLayout()

        control_hbox.addStretch()

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        self.start_stop_button = QPushButton("Stop")
        self.start_stop_button.clicked.connect(self.toggle_stop)

        control_hbox.addWidget(reset_button)
        control_hbox.addWidget(self.start_stop_button)

        main_vbox.addLayout(control_hbox)

        ip_hbox = QHBoxLayout()
        ip_hbox.setAlignment(Qt.AlignCenter)

        ip_address = self.getIPAddress()
        ip_label = QLabel("Host IP Address: {}".format(ip_address))
        newfont = QFont("Ubuntu", 15, QFont.Bold) 
        ip_label.setFont(newfont)
        ip_hbox.addWidget(ip_label)

        main_vbox.addLayout(ip_hbox)

        self.setLayout(main_vbox)
        self.setGeometry(200,100,700,700)

        t = threading.Thread(target=self.run_host, args=(ip_address,))
        t.start()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)

        # draw lines

        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)

        for i in range(5):
            y = 300 + 30 * i
            qp.drawLine(100, y, 1700, y)
    
        for i in range(5):
            y = 300 + (2 * 120) + 30 * i
            qp.drawLine(100, y, 1700, y)

        qp.drawLine(100, 300, 100, 660)
        qp.drawLine(1700, 300, 1700, 660)


        # draw moving line
        time = (host.FoxDotHandler.getTime() * 1600 / 4) % 1600 + 100

        pen = QPen(Qt.blue, 4, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(time, 300, time, 660)

        #draw images
        # clefs

        script_dir = os.path.dirname(__file__) # hard to read, should be in for loop
        file_paths = ["trebel_clef.png", "bass_clef.png"]
        rel_paths = ["assets/" + file for file in file_paths]
        abs_file_path = [os.path.join(script_dir, p) for p in rel_paths]

        treble = QPixmap(abs_file_path[0])
        bass = QPixmap(abs_file_path[1])

        qp.drawPixmap(110, 280, 64, 160, treble)
        qp.drawPixmap(110, 547, 80, 100, bass)

        qp.end()


    def getIPAddress(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = (s.getsockname()[0])
        s.close()
        return ip_address

    def reset(self):
        host.FoxDotHandler.stop()
        host.FoxDotHandler.stop()
        return

    def toggle_stop(self):
        start = "Start"
        stop = "Stop"

        if self.start_stop_button.text() == start: # stop
            host.FoxDotHandler.stop()
            self.start_stop_button.setText(stop)
        else:
            self.start_stop_button.setText(start)

    def run_host(self, address):
        self.host.setup_socket(address)
        self.host.listen()

    def update_1(self):
        while True:
            self.update()               
            QApplication.processEvents()
            time.sleep(0.0025)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HostWidget()
    window.setGeometry(100,100,1900,1300)
    window.show()
    window.update_1()
    sys.exit(app.exec_())