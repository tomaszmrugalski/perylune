#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QVBoxLayout, QLabel, \
     QLineEdit, QTabWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5.QtCore import pyqtSlot

from OrbCalc import *

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

        self.b1 = QLineEdit() # longitude (dlugosc)
        self.l1 = QLineEdit() # lattitude (szerokosc)

        self.pktA_box.layout.addWidget(b1title, 1, 0)
        self.pktA_box.layout.addWidget(self.b1, 1, 1)

        self.pktA_box.layout.addWidget(l1title, 2, 0)
        self.pktA_box.layout.addWidget(self.l1, 2, 1)

        # Setting up form for the second point
        self.pktB_box = QGroupBox('Second point')
        self.pktB_box.layout = QGridLayout(self.pktB_box)
        self.pktB_box.setLayout(self.pktB_box.layout)

        vbox.addWidget(self.pktB_box, 0)
        b2title = QLabel('Longitude (B)')
        l2title = QLabel('Lattitude (L)')
        self.b2 = QLineEdit() # longitude (dlugosc)
        self.l2 = QLineEdit() # lattitude (szerokosc)

        self.pktB_box.layout.addWidget(b2title, 1, 0)
        self.pktB_box.layout.addWidget(self.b2, 1, 1)

        self.pktB_box.layout.addWidget(l2title, 2, 0)
        self.pktB_box.layout.addWidget(self.l2, 2, 1)

        # Set the calc button
        self.calc_btn = QPushButton("Calculate!")
        vbox.addWidget(self.calc_btn, 0)
        self.calc_btn.clicked.connect(self.on_calc_click)

        # Set the output box
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        vbox.addWidget(self.text, 0)

        vbox.addStretch(2)

        x.setLayout(vbox)
        return x

    @pyqtSlot()
    def on_calc_click(self):

        # Get the input data (point A)
        b1_text = self.b1.text()
        l1_text = self.l1.text()

        # Get the input data (point B)
        b2_text = self.b2.text()
        l2_text = self.l2.text()

        # Parse longitude and convert to a float
        b1_long = OrbCalc.parseLongitude(b1_text)
        b1_float = OrbCalc.longitudeToFloat(b1_long)
        l1_long = OrbCalc.parseLongitude(l1_text)
        l1_float = OrbCalc.longitudeToFloat(l1_long)

        b2_long = OrbCalc.parseLongitude(b2_text)
        b2_float = OrbCalc.longitudeToFloat(b2_long)
        l2_long = OrbCalc.parseLongitude(l2_text)
        l2_float = OrbCalc.longitudeToFloat(l2_long)



        self.setText("Point A (%d %d %f, %d %d %f) is really %f %f\n"
                         % (b1_long[0], b1_long[1], b1_long[2],
                            l1_long[0], l1_long[1], l1_long[2],
                            b1_float, l1_float))

        self.addText("Point B (%d %d %f, %d %d %f) is really %f %f\n"
                         % (b2_long[0], b2_long[1], b2_long[2],
                            l2_long[0], l2_long[1], l2_long[2],
                            b2_float,   l2_float))

    def setText(self, txt):
        self.text.setText(txt)

    def addText(self, txt):
        txt = self.text.toPlainText() + txt
        self.text.setText(txt)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    c = CalcGUI(sys.argv)
    c.run()
    sys.exit(app.exec_())
