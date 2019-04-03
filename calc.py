#

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QVBoxLayout, QLabel, \
     QLineEdit, QTabWidget, QPushButton, QGroupBox

# from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot

class CalcGUI(QMainWindow):

    def __init__(self, argv):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.title = 'OrbCalc'
        self.left = 0
        self.top = 0
        self.width = 1024
        self.height = 768
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = CalcGUITabs(self)
        self.setCentralWidget(self.table_widget)

        # Move the window to the center
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
 
    def run(self):

        self.show()

class CalcGUITabs(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = self.initSphericalDistanceUI()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Spherical distance")
        self.tabs.addTab(self.tab2, "RA/Dec")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # Initialize 
    def initSphericalDistanceUI(self):
        x = QWidget()
        vbox = QVBoxLayout(self)
        vbox.setSpacing(10)

        # Setting up form for the first point
        self.pktA_box = QGroupBox('First point')
        self.pktA_box.layout = QGridLayout(self.pktA_box)
        self.pktA_box.setLayout(self.pktA_box.layout)

        vbox.addWidget(self.pktA_box, 0)

        b1title = QLabel('Longitude (B)')
        l1title = QLabel('Lattitude (L)')

        b1 = QLineEdit() # longitude (dlugosc)
        l1 = QLineEdit() # lattitude (szerokosc)
        
        self.pktA_box.layout.addWidget(b1title, 1, 0)
        self.pktA_box.layout.addWidget(b1, 1, 1)

        self.pktA_box.layout.addWidget(l1title, 2, 0)
        self.pktA_box.layout.addWidget(l1, 2, 1)

        # Setting up form for the second point
        self.pktB_box = QGroupBox('Second point')
        self.pktB_box.layout = QGridLayout(self.pktB_box)
        self.pktB_box.setLayout(self.pktB_box.layout)

        vbox.addWidget(self.pktB_box, 0)
        b2title = QLabel('Longitude (B)')
        l2title = QLabel('Lattitude (L)')
        b2 = QLineEdit() # longitude (dlugosc)
        l2 = QLineEdit() # lattitude (szerokosc)

        self.pktB_box.layout.addWidget(b2title, 1, 0)
        self.pktB_box.layout.addWidget(b2, 1, 1)

        self.pktB_box.layout.addWidget(l2title, 2, 0)
        self.pktB_box.layout.addWidget(l2, 2, 1)
        
        #grid.addWidget(b2title, 3, 0)
        #grid.addWidget(b2, 3, 1)

        #grid.addWidget(l2title, 4, 0)
        #grid.addWidget(l2, 4, 1)

        vbox.addStretch(2)

        x.setLayout(vbox)
        return x

if __name__ == '__main__':

    app = QApplication(sys.argv)
    c = CalcGUI(sys.argv)
    c.run()
    sys.exit(app.exec_())
