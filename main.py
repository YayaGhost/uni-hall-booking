import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from firebase_manager import FirebaseManager
from pathlib import Path

class HallBookingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hall Booking System")
        self.resize(1200, 720)
        self.is_dark_mode = True
        
        #app main container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget) #vbox arranges widgets top to bottom
        
        #header title and theme toggle button
        header_layout = QHBoxLayout()
        self.title = QLabel("Hall Booking System")
        self.title.setObjectName("titleText")

        self.theme_btn = QPushButton()
        self.theme_btn.setStyle
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        base_dir = Path(__file__).parent
        self.dark_mode = str(base_dir / "assets" / "dark_mode.svg")
        self.light_mode = str(base_dir / "assets" / "light_mode.svg")
        self.theme_btn.setIcon(QIcon(self.light_mode))
        self.theme_btn.setIconSize(QSize(24, 24))
        self.theme_btn.setFixedSize(QSize(40, 40))
        
        
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        self.layout.addLayout(header_layout)
        
        #hall booking in a grid layout
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
        self.hall_buttons = {}
        
        self.db_manager = FirebaseManager()
        self.db_manager.halls_updated.connect(self.update_halls)
        self.db_manager.start_listener()
        
        self.layout.addStretch()
        self.apply_theme()
        
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()
    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #161512; color: #bababa; font-family: Arial; }
                QLabel#titleText { font-size: 32px; font-weight: bold; color: #ffffff; }
                QPushButton { border: none; border-radius: 4px; padding: 20px; font-weight: bold; font-size: 24px; }
                QPushButton#themeBtn { border-radius: 20px; background-color: #161512; color: #bababa; padding: 10px; }
                QPushButton#themeBtn:hover { background-color: #363431; color: #ffffff; }
                QPushButton#available { background-color: #629924; color: white; }
                QPushButton#available:hover { background-color: #72a934; }
                QPushButton#booked { background-color: #302e2b; color: #666666; }
            """)
            self.theme_btn.setIcon(QIcon(self.light_mode))
        else:
            self.setStyleSheet("""
                QWidget { background-color: #edebe9; color: #2b2b2b; font-family: Arial; }
                QLabel#titleText { font-size: 32px; font-weight: bold; color: #2b2b2b; }
                QPushButton { border: none; border-radius: 4px; padding: 20px; font-weight: bold; font-size: 24px; }
                QPushButton#themeBtn { border-radius: 20px; background-color: #edebe9; color: #2b2b2b; padding: 10px; }
                QPushButton#themeBtn:hover { background-color: #e0e0e0; }
                QPushButton#available { background-color: #7fb041; color: white; }
                QPushButton#available:hover { background-color: #8fc051; }
                QPushButton#booked { background-color: #cccccc; color: #888888; }
            """)
            self.theme_btn.setIcon(QIcon(self.dark_mode))
        
    def update_halls(self,live_data):
        halls = sorted(live_data.keys())
        for hall_id in halls:
            status = live_data[hall_id]
            if hall_id not in self.hall_buttons:
                btn = QPushButton()
                btn.setFixedSize(QSize(234,133))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                self.hall_buttons[hall_id] = btn
                
                btn.clicked.connect(lambda checked, h=hall_id: self.confirm_booking(h))
                
                count = len(self.hall_buttons) - 1
                row = count // 3
                col = count % 3
                self.grid_layout.addWidget(btn, row, col)
            
            btn = self.hall_buttons[hall_id]
            if status == "available":
                btn.setObjectName("available")
                btn.setText(f"{hall_id}\nAvailable")
                btn.setEnabled(True)
            else:
                btn.setObjectName("booked")
                btn.setText(f"{hall_id}\nBooked")
                btn.setEnabled(False)
        self.apply_theme()
        
    def confirm_booking(self, hall_id):
        reply = QMessageBox.question(
            self, "Confirm Booking",
            f"Do you want to book {hall_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.book_hall(hall_id)
            if not success:
                QMessageBox.critical(self, "Booking Failed", msg)

if __name__ == "__main__":
    app = QApplication([])
    window = HallBookingUI()
    window.show()
    sys.exit(app.exec())