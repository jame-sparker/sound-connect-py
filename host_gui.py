import sys
import os
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import host
import time
import music

class HostWidget(QWidget):
    def __init__(self, parent=None):
        super(HostWidget, self).__init__(parent)

        self.host = host.Host()
        self.running = True
        self.start_on = True

        # set background color

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        
        main_vbox = QVBoxLayout()
        main_vbox.setMargin(50)
        main_vbox.addStretch() ## temporary

        control_hbox = QHBoxLayout()


        control_hbox.addStretch()

        measures_label = QLabel("Measures")
        control_hbox.addWidget(measures_label)

        measures_up_button = QPushButton("^")
        measures_down_button = QPushButton("v")
        measures_up_button.clicked.connect(host.FoxDotHandler.increment_measure)
        measures_down_button.clicked.connect(host.FoxDotHandler.decrement_measure)

        control_hbox.addWidget(measures_up_button)
        control_hbox.addWidget(measures_down_button)


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
        newfont = QFont("Ubuntu", 20, QFont.Bold) 
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
        sheet_width = width - 2 * side_margin
        clef_width = 100
        usable_sheet_width = sheet_width - clef_width

        measures = host.FoxDotHandler.get_measure()

        # draw horizontal lines
        for i in range(5):
            y = top + line_space * i
            qp.drawLine(side_margin, y, width - side_margin, y)
    
        for i in range(5):
            y = top + ((8 + i) * line_space)
            qp.drawLine(side_margin, y, width - side_margin, y)

        qp.drawLine(side_margin, bottom + 2 * line_space, width - side_margin, bottom + 2 * line_space)

        # draw vertical lines

        x = side_margin
        qp.drawLine(x, top, x, bottom)

        for i in range(1, measures + 1):
            x = side_margin + clef_width + i * (usable_sheet_width) / measures
            qp.drawLine(x, top, x, bottom)

        # draw moving line

        if self.start_on:
            time_ratio = (host.FoxDotHandler.getTime() % measures) / measures
            time_x = (time_ratio * usable_sheet_width) + side_margin + clef_width

            pen = QPen(Qt.blue, 4, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(time_x, top, time_x, bottom + 2 * line_space)

        #draw images
        # clefs

        script_dir = os.path.dirname(__file__) # hard to read, should be in for loop
        file_paths = ["trebel_clef.png", "bass_clef.png"]
        rel_paths = ["assets/" + file for file in file_paths]
        abs_file_path = [os.path.join(script_dir, p) for p in rel_paths]

        treble = QPixmap(abs_file_path[0])
        bass = QPixmap(abs_file_path[1])

        qp.drawPixmap(110, top - 20, 64, 160, treble)
        qp.drawPixmap(110, bottom - 113, 80, 100, bass)

        # user instruments

        # create image list
        instrument_images = []

        for inst in music.instrument_names:
            image_file_name = inst + ".png"
            rel_path = "assets/" + image_file_name
            abs_file_path = os.path.join(script_dir, rel_path)
            instrument_images.append(QPixmap(abs_file_path))

        for _, _, input_args in host.FoxDotHandler.players.values():

            timing, inst_index, pitch, nickname = input_args

            y = 0
            
            if inst_index <= 8 and inst_index >= 4: # drum kit
                y = bottom + 2 * line_space
            else:
                if pitch >= 0:
                    y = top + line_space * 5 - (line_space / 2) * pitch
                else: 
                    y = top + line_space * 7.5 - (line_space / 2) * pitch

            for x_timing in timing:
                x = (x_timing / measures * usable_sheet_width + clef_width + side_margin)

                size = 40 
                if self.start_on:
                    size = max(size, 60 - abs(time_x - x))

                qp.drawPixmap(x - size /2, y - size / 2, size, size, instrument_images[inst_index])
                pen = QPen(QColor(216, 67, 8), 4, Qt.SolidLine)
                qp.setPen(pen)
                qp.drawText(x - 25, y + 25,  nickname)

        qp.end()


    def getIPAddress(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8",80))
            ip_address = (s.getsockname()[0])
            s.close()
            return ip_address
        except:
            return ""

    def reset(self):
        host.FoxDotHandler.reset()
        return

    def toggle_stop(self):

        if not self.start_on:

            host.FoxDotHandler.restart()
            self.start_stop_button.setText("Stop")
        else:
            host.FoxDotHandler.stop()
            self.start_stop_button.setText("Start")

        self.start_on = not self.start_on

    def run_host(self, address):
        self.host.setup_socket(address)
        self.host.listen()

    def update_1(self):
        while True:
            self.update()               
            QApplication.processEvents()
            time.sleep(0.001)

    def closeEvent(self, event): # perform clean up
        # self.running = False
        self.host.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HostWidget()
    window.setGeometry(100,100,1900,1300)
    window.show()
    window.update_1()
    sys.exit(app.exec_())