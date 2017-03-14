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
        self.running = True
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

        self.t = threading.Thread(target=self.run_host, args=(ip_address,))
        self.t.start()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)

        # draw lines

        pen = QPen(Qt.black, 3, Qt.SolidLine)
        qp.setPen(pen)

        height = self.frameGeometry().height()
        width = self.frameGeometry().width()
        top = height / 2 - 200
        line_space = 30
        bottom = top + line_space * 12
        side_margin = 100


        for i in range(5):
            y = top + line_space * i
            qp.drawLine(side_margin, y, width - side_margin, y)
    
        for i in range(5):
            y = top + ((8 + i) * line_space)
            qp.drawLine(side_margin, y, width - side_margin, y)

        qp.drawLine(side_margin,
                    top,
                    side_margin,
                    bottom)

        qp.drawLine(width - side_margin,
                    top,
                    width - side_margin, 
                    bottom)


        # draw moving line

        sheet_width = width - 2 * side_margin
        measures = 4

        time = (host.FoxDotHandler.getTime() * sheet_width / measures) % sheet_width + side_margin

        pen = QPen(Qt.blue, 4, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(time, top, time, bottom)

        #draw images
        # clefs

        script_dir = os.path.dirname(__file__) # hard to read, should be in for loop
        file_paths = ["trebel_clef.png", "bass_clef.png"]
        rel_paths = ["assets/" + file for file in file_paths]
        abs_file_path = [os.path.join(script_dir, p) for p in rel_paths]

        treble = QPixmap(abs_file_path[0])
        bass = QPixmap(abs_file_path[1])

        qp.drawPixmap(110, top - 20, 64, 160, treble)
        qp.drawPixmap(110, bottom - 83, 80, 100, bass)

        # draw points

        qp.end()


    def getIPAddress(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = (s.getsockname()[0])
        s.close()
        return ip_address

    def reset(self):
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
        while self.running:
            self.update()               
            QApplication.processEvents()
            time.sleep(0.0025)
        print "update done"

    def closeEvent(self, event):
        window.running = False
        window.host.stop()
        print ("close finish")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HostWidget()
    window.setGeometry(100,100,1900,1300)
    window.show()
    print threading.enumerate()
    sys.exit(app.exec_())
    window.update_1()