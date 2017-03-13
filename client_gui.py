import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import socket

import client


class Client_Gui:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.win = QWidget()

        self.client = client.Client()

    def getIPAddress(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = (s.getsockname()[0])
        s.close()
        return ip_address

    def show_connection_window(self):

        main_vbox = QVBoxLayout()
        main_vbox.setMargin(50)

        fbox = QFormLayout()

        l1 = QLabel("Nickname:")
        name_edit = QLineEdit()
        fbox.addRow(l1,name_edit)

        l2 = QLabel("Host IP Address:")
        ip_edit = QLineEdit()


        fbox.addRow(l2,ip_edit)
        main_vbox.addLayout(fbox)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)

        error_text = QLabel("")
        

        def connect_clicked():
            nickname = str(name_edit.text()).strip()
            host_ip = str(ip_edit.text()).strip()
            try:
                error_text.setStyleSheet('color: gray')
                error_text.setText("Connecting")
                self.client.connect(host = host_ip)
            except:
                error_text.setStyleSheet('color: red')
                error_text.setText("Connection failed")
            print("")


        connect = QPushButton("Connect")
        connect.setFixedWidth(100)
        connect.clicked.connect(connect_clicked)

        hbox.addWidget(connect)
        main_vbox.addLayout(hbox)

        ip_hbox = QHBoxLayout()
        ip_hbox.setAlignment(Qt.AlignCenter)

        l3 = QLabel("Your IP Address: {}".format(self.getIPAddress()))
        ip_hbox.addWidget(l3)

        main_vbox.addLayout(ip_hbox)

        error_hbox = QHBoxLayout()
        error_hbox.setAlignment(Qt.AlignCenter)

        error_hbox.addWidget(error_text)

        main_vbox.addLayout(error_hbox)

        self.win.setLayout(main_vbox)
        
        self.win.setGeometry(100,100,500,300)
        self.win.setWindowTitle("SoundConnectPy")
        self.win.show()
        sys.exit(self.app.exec_())

    def show_music_window():

        main_hbox = QHBoxLayout()
        main_hbox.setMargin(50)

        instrument_vbox = QVBoxLayout()

        instrument_image = QLabel()
        instrument_image.setPixmap(QPixmap("python.jpg"))

        cb = QComboBox()
        cb.addItem("Piano")

        instrument_vbox.addWidget(instrument_image)
        instrument_vbox.addWidget(cb)

        main_hbox.addLayout(instrument_vbox)


        details_vbox = QVBoxLayout()
        
        

        # script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        # rel_path = "assets/music.png"
        # abs_file_path = os.path.join(script_dir, rel_path)


        self.win.setLayout(main_hbox)
        
        self.win.setGeometry(100,100,500,500)


if __name__ == '__main__':
    gui = Client_Gui()
    gui.show_connection_window()