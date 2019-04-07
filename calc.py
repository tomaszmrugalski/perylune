#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QVBoxLayout, QLabel, \
     QLineEdit, QTabWidget, QPushButton, QGroupBox, QTextEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from OrbCalc import *
from math import sin, cos, asin, acos, sqrt

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
        self.tab1 = self.initOrbitalElementsUI()
        self.tab2 = self.initSphericalDistanceUI()

        # Add tabs
        self.tabs.addTab(self.tab1, "Orbital elements")
        self.tabs.addTab(self.tab2, "Spherical distance")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.fillSampleData()

    def fillSampleData(self):
        self.b1.setText("54 31 35,4")
        self.l1.setText("18 30 38,3")
        self.b2.setText("52 12 0,9")
        self.l2.setText("21 0 34,6")

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
        self.text.resize(self.text.width(), self.text.height() + 800)

        x.setLayout(vbox)
        return x

    def initOrbitalElementsUI(self):
        x = QWidget()
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Setting up group 1: handling almanac loading from file
        almanac = QGroupBox('Almanac')
        almanac.layout = QGridLayout(almanac)
        almanac.setLayout(almanac.layout)

        # Almanac filename to be loaded.
        almanac.load_btn = QPushButton("Load alamanac")
        almanac.layout.addWidget(almanac.load_btn, 0,0)

        almanac_name = 'data/almanac.yuma.week0000.061440.txt'
        almanac.layout.addWidget(QLabel(almanac_name), 0,1)

        almanac.combo_box = QComboBox()
        almanac.layout.addWidget(almanac.combo_box, 1,0,2,0)

        x.almanac = almanac

        layout.addWidget(almanac, 0)

        # Group 2: Keplerian elements
        keplerian = QGroupBox('Keplerian elements')

        keplerian.layout = QGridLayout(keplerian)
        keplerian.layout.setSpacing(1)

        # element 1: eccentricity
        keplerian.layout.addWidget(QLabel('Eccentricity [none]'), 0, 0)
        keplerian.e = QLineEdit()
        keplerian.layout.addWidget(keplerian.e, 0,1)

        # element 2: time of applicability [s]
        keplerian.layout.addWidget(QLabel('Time of applicability [s]'), 1, 0)
        keplerian.toa = QLineEdit()
        keplerian.layout.addWidget(keplerian.toa, 1,1)

        # element 3: inclination [rad]
        keplerian.layout.addWidget(QLabel('Inclination [rad]'), 2, 0)
        keplerian.incl = QLineEdit()
        keplerian.layout.addWidget(keplerian.incl, 2,1)

        # element 4: Rate of Right Ascension [rad/s]
        keplerian.layout.addWidget(QLabel('Rate of Right Ascension [rad/s]'), 3, 0)
        keplerian.ra_rate = QLineEdit()
        keplerian.layout.addWidget(keplerian.ra_rate, 3,1)

        # element 5: sqrt(A) [m ^ 1/2]
        keplerian.layout.addWidget(QLabel('Sq. root of major semi-axis [m^1/2]'), 4, 0)
        keplerian.sqrt_a = QLineEdit()
        keplerian.layout.addWidget(keplerian.sqrt_a, 4,1)

        # element 6: Right ascension at week [rad]
        keplerian.layout.addWidget(QLabel('Right ascension at week [rad]'), 5, 0)
        keplerian.ra_week = QLineEdit()
        keplerian.layout.addWidget(keplerian.ra_week, 5, 1)

        # element 7: Argument of perigee [rad]
        keplerian.layout.addWidget(QLabel('Argument of perigee [rad]'), 6, 0)
        keplerian.aop = QLineEdit()
        keplerian.layout.addWidget(keplerian.aop, 6, 1)

        # element 8: Mean anomaly [rad]
        keplerian.layout.addWidget(QLabel('Mean anomaly [rad]'), 7, 0)
        keplerian.mean_anomaly = QLineEdit()
        keplerian.layout.addWidget(keplerian.mean_anomaly, 7, 1)

        self.keplerian = keplerian

        layout.addWidget(keplerian,1)


        calc_btn = QPushButton("Calculate!")
        layout.addWidget(calc_btn, 0)
        calc_btn.clicked.connect(self.on_kepler_calc_click)

        # Group 3: Set the output box
        x.text = QTextEdit()
        x.text.setReadOnly(True)
        layout.addWidget(x.text, 2)
        x.text.resize(x.text.width(), x.text.height() + 800)

        x.setLayout(layout)
        return x

    @pyqtSlot()
    def on_kepler_calc_click(self):
        pass

    @pyqtSlot()
    def on_calc_click(self):

        # Get the input data (point A)
        b1_text = self.b1.text()
        l1_text = self.l1.text()

        # Get the input data (point B)
        b2_text = self.b2.text()
        l2_text = self.l2.text()

        # Parse longitude and convert to a float
        b1_text = OrbCalc.parseLongitude(b1_text)
        b1 = OrbCalc.longitudeToFloat(b1_text)
        l1_text = OrbCalc.parseLongitude(l1_text)
        l1 = OrbCalc.longitudeToFloat(l1_text)

        b2_text = OrbCalc.parseLongitude(b2_text)
        b2 = OrbCalc.longitudeToFloat(b2_text)
        l2_text = OrbCalc.parseLongitude(l2_text)
        l2 = OrbCalc.longitudeToFloat(l2_text)

        # Print the entry points
        self.setText("Point A (%d %d %f, %d %d %f) in floating point notation is %f, %f\n"
                         % (b1_text[0], b1_text[1], b1_text[2],
                            l1_text[0], l1_text[1], l1_text[2],
                            b1, l1))

        self.addText("Point B (%d %d %f, %d %d %f) in floating point notation is %f, %f\n"
                         % (b2_text[0], b2_text[1], b2_text[2],
                            l2_text[0], l2_text[1], l2_text[2],
                            b2,   l2))

        # Convert longitude, lattitude to radians
        b1 = OrbCalc.deg2rad(b1)
        b2 = OrbCalc.deg2rad(b2)
        l1 = OrbCalc.deg2rad(l1)
        l2 = OrbCalc.deg2rad(l2)

        #
        # self.addText("B1rad=%f L1rad=%f B2rad=%f L2rad=%f" % (b1, l1, b2, l2))

        #
        bsr = (b1+b2)/2

        cosd = sin(b1)*sin(b2) + cos(b1)*cos(b2)*cos(l2 - l1)
        d = acos(cosd)

        self.addText("cos(D)=%f d=%f [rad] d=%f [deg]\n" % (cosd, d, OrbCalc.rad2deg(d)))

        a = OrbCalc.getConst('earth-radius')
        f = OrbCalc.getConst('earth-flattening')

        # e^2
        esquare = 2*f - f*f

        expr1 = 1 - esquare*(sin(bsr)*sin(bsr))
        expr = expr1*expr1*expr1
        expr = sqrt(expr)

        M = a*(1-esquare)/expr
        N = a/sqrt(expr1)

        avg_radius_of_ellipsoid = sqrt(N*M)

        dist = d*avg_radius_of_ellipsoid

        self.addText("expr=%f, M=%f N=%f avg-radius=%f distance=%f\n" % (expr, M, N, avg_radius_of_ellipsoid, dist))

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
