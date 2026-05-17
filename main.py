import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout)
from PyQt6.QtCore import Qt

class HallBookingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hall Booking System")
        self.resize(854, 480)
        self.is_dark_mode = True
        