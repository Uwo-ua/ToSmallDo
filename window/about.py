
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QPushButton)
from PyQt5 import uic
import sys


textAbout = """
This is a test project. It does not make much sense. \nCreated for learning and nothing more
"""

class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()
        uic.loadUi("window/about.ui", self)
        self.label = self.findChild(QLabel, "label")
        self.label.setText(textAbout)
        self.closebtn = self.findChild(QPushButton, "closeBtn")
        self.closebtn.clicked.connect(self.close)
    def show_(self):
        self.show()




