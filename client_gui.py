import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import socket
import client
import music


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
        self.parent = parent

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

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return: 
            self.parent.connect_clicked()
        else:
            super(ConnectionWidget,self).keyPressEvent(qKeyEvent)


class MusicWidget(QWidget):

    def __init__(self, parent=None):

        super(MusicWidget, self).__init__(parent)
        self.parent = parent
        
        back_button = QPushButton(self)
        back_button.setGeometry(10,10,60,30)
        back_button.setText("< Back")
        back_button.clicked.connect(parent.return_clicked)

        self.error_label = QLabel(self)
        self.error_label.setGeometry(200,390,200,30)
        self.error_label.setStyleSheet('color: red')


        main_hbox = QHBoxLayout()
        main_hbox.setMargin(50)

        instrument_vbox = QVBoxLayout()

        self.instrument_image = QLabel()
        self.instrument_image.setFixedWidth(300)
        self.instrument_image.setFixedHeight(300)
        self.instrument_image.setScaledContents(True)


        self.instrument_cb = QComboBox()

        # add items to combobox
        self.instrument_cb.addItems(music.instrument_display_names)
        self.instrument_cb.currentIndexChanged.connect(self.setComboBoxImage)


        self.setComboBoxImage()

        instrument_vbox.addWidget(self.instrument_image)
        instrument_vbox.addWidget(self.instrument_cb)

        main_hbox.addLayout(instrument_vbox)

        details_vbox = QVBoxLayout()

        pitch_hbox = QHBoxLayout()
        
        pitch_label = QLabel("Note:")
        pitch_hbox.addWidget(pitch_label)

        self.pitch_cb = QComboBox()
        self.pitch_cb.addItems(music.allnotes)
        self.pitch_cb.setMaxVisibleItems(15)
        self.pitch_cb.setCurrentIndex(12)
        self.pitch_cb.setStyleSheet("QComboBox { combobox-popup: 0; }");

        pitch_hbox.addWidget(self.pitch_cb)

        pitch_hbox.addStretch()

        details_vbox.addLayout(pitch_hbox)

        timing = QLabel("Timing:")
        details_vbox.addWidget(timing)
        self.timing_edit = QLineEdit()
        details_vbox.addWidget(self.timing_edit)

        details_vbox.addStretch()

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_clicked)
        details_vbox.addWidget(send_button)

        main_hbox.addLayout(details_vbox)

        self.setLayout(main_hbox)
        self.setGeometry(100,100,550,500)


    def setComboBoxImage(self):

        index = self.instrument_cb.currentIndex()

        image_file_name = music.instrument_names[index] + ".png"
        script_dir = os.path.dirname(__file__)
        rel_path = "assets/" + image_file_name
        abs_file_path = os.path.join(script_dir, rel_path)
        self.instrument_image.setPixmap(QPixmap(abs_file_path))

    def send_clicked(self):

        timing_text = str(self.timing_edit.text()).replace(" ", "")

        if self.is_valid_timing(timing_text):
            self.error_label.setText("")
            note_text = str(self.pitch_cb.currentText())
            
            index = self.instrument_cb.currentIndex()
            instrument_text = music.instrument_names[index]

            message = note_text + "|" + instrument_text + "|" + timing_text
            self.parent.client.send(message)

        else:
            self.error_label.setText("Invalid timing input")

    def is_valid_timing(self, text):

        try:
            for text_num in text.split(","):
                n, d = map(float, text_num.split("/"))
                n / d
        except:
            return False
        return True

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return: 
            self.send_clicked()
        else:
            super(MusicWidget, self).keyPressEvent(qKeyEvent)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100,100,400,300)
    window.show()
    # app.exec_()
    sys.exit(app.exec_())