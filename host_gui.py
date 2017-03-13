import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class HostWidget(QWidget):
    def __init__(self, parent=None):
        super(HostWidget, self).__init__(parent)
        
        main_hbox = QHBoxLayout()

        self.setLayout(main_hbox)
        self.setGeometry(100,100,500,500)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HostWidget()
    window.setGeometry(100,100,100,100)
    window.show()
    # app.exec_()
    sys.exit(app.exec_())