import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import socket
import client


class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.connection_widget = ConnectionWidget(self)
        self.central_widget.addWidget(self.connection_widget)

        self.client = client.Client()

    def connect_clicked(self):
        nickname = str(self.connection_widget.name_edit.text()).strip()
        host_ip = str(self.connection_widget.ip_edit.text()).strip()
        try:
            error_text = self.connection_widget.error_text
            error_text.setStyleSheet('color: gray')
            error_text.setText("Connecting")

            self.client.connect(host = host_ip)

            error_text.setText("")

            music_widget = MusicWidget(self)
            self.central_widget.addWidget(music_widget)
            self.central_widget.setCurrentWidget(music_widget)

        except Exception as e: 
            print(e)

            error_text.setStyleSheet('color: red')
            error_text.setText("Connection failed")

    def return_clicked(self):
        self.client.close()
        self.central_widget.setCurrentWidget(self.connection_widget)

class ConnectionWidget(QWidget):
    def __init__(self, parent=None):
        super(ConnectionWidget, self).__init__(parent)

        main_vbox = QVBoxLayout()
        main_vbox.setMargin(50)

        fbox = QFormLayout()

        l1 = QLabel("Nickname:")
        self.name_edit = QLineEdit()
        fbox.addRow(l1, self.name_edit)

        l2 = QLabel("Host IP Address:")
        self.ip_edit = QLineEdit()


        fbox.addRow(l2, self.ip_edit)
        main_vbox.addLayout(fbox)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)

        self.error_text = QLabel("")

        connect = QPushButton("Connect")
        connect.setFixedWidth(100)
        connect.clicked.connect(parent.connect_clicked)

        hbox.addWidget(connect)
        main_vbox.addLayout(hbox)

        ip_hbox = QHBoxLayout()
        ip_hbox.setAlignment(Qt.AlignCenter)

        l3 = QLabel("Your IP Address: {}".format(self.getIPAddress()))
        ip_hbox.addWidget(l3)
        l3.setTextInteractionFlags(Qt.TextSelectableByMouse)

        main_vbox.addLayout(ip_hbox)

        error_hbox = QHBoxLayout()
        error_hbox.setAlignment(Qt.AlignCenter)

        error_hbox.addWidget(self.error_text)

        main_vbox.addLayout(error_hbox)


        self.setGeometry(100,100,500,300)
        self.setWindowTitle("SoundConnectPy")
        self.setLayout(main_vbox)

    def getIPAddress(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip_address = (s.getsockname()[0])
        s.close()
        return ip_address


class MusicWidget(QWidget):
    def __init__(self, parent=None):
        super(MusicWidget, self).__init__(parent)
        
        back_button = QPushButton(self)
        back_button.setGeometry(10,10,60,30)
        back_button.setText("< Back")
        back_button.clicked.connect(parent.return_clicked)

        main_hbox = QHBoxLayout()
        main_hbox.setMargin(50)

        instrument_vbox = QVBoxLayout()

        instrument_image = QLabel()
        instrument_image.setPixmap(QPixmap("music.png"))

        instrument_cb = QComboBox()
        instrument_cb.addItem("Piano")

        instrument_vbox.addWidget(instrument_image)
        instrument_vbox.addWidget(instrument_cb)

        main_hbox.addLayout(instrument_vbox)

        details_vbox = QVBoxLayout()

        pitch_hbox = QHBoxLayout()
        
        pitch_label = QLabel("Note:")
        pitch_hbox.addWidget(pitch_label)

        pitch_cb = QComboBox()
        pitch_cb.addItem("C4")
        pitch_hbox.addWidget(pitch_cb)

        pitch_hbox.addStretch()

        details_vbox.addLayout(pitch_hbox)

        timing = QLabel("Timing")
        details_vbox.addWidget(timing)
        timing_edit = QLineEdit()
        details_vbox.addWidget(timing_edit)

        details_vbox.addStretch()

        send_button = QPushButton("Send")
        details_vbox.addWidget(send_button)

        main_hbox.addLayout(details_vbox)

        self.setLayout(main_hbox)
        self.setGeometry(100,100,500,500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100,100,0,0)
    window.show()
    # app.exec_()
    sys.exit(app.exec_())