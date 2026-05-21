import sys
from functools import partial
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from firebase_manager import FirebaseManager
from pathlib import Path

class HallBookingUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hall Booking System")
        self.resize(732, 660)
        self.setMinimumSize(732, 660)
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

        #Time slot tab bar
        self.periods = ['08:30 AM - 10:00 AM','10:15 AM - 11:45 AM',
                        '12:15 PM - 01:45 PM','02:00 PM - 03:30 PM',
                        '03:30 PM - 05:00 PM']
        self.current_period = self.periods[0]
        self.tab_buttons = {}
        
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(0)

        for period in self.periods:
            btn = QPushButton(period)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            if period == self.current_period:
                btn.setObjectName("activeTab")
            else:
                btn.setObjectName("inactiveTab")
            
            btn.clicked.connect(partial(self.switch_period, period))
            self.tab_buttons[period] = btn
            tab_layout.addWidget(btn)
        
        self.layout.addLayout(tab_layout)
        self.last_live_data = {}
        
        #hall booking in a grid layout
        #horizontal container for clean packed together buttons
        grid_container = QHBoxLayout()
        grid_container.addStretch()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(6)
        grid_container.addLayout(self.grid_layout)
        grid_container.addStretch()
        self.layout.addLayout(grid_container)

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
                QPushButton#booked:hover { background-color: #8C1A10; color: #666666; }
                QPushButton#activeTab { font-size: 12px; background-color: #302e2b; color: #ffffff; border-radius: 0px; padding: 10px 5px; font-weight: bold; border-bottom: 3px solid #629924; }
                QPushButton#inactiveTab { font-size: 12px; background-color: transparent; color: #888888; border-radius: 0px; padding: 10px 5px; font-weight: bold; }
                QPushButton#inactiveTab:hover { background-color: #262421; color: #bababa; }
                QMessageBox { background-color: #262421; }
                QMessageBox QLabel { background-color: transparent; color: #ffffff; font-size: 14px; font-weight: normal; }
                QMessageBox QPushButton { background-color: #302e2b; color: #bababa; border-radius: 3px; padding: 8px 15px; min-width: 80px; font-size: 13px; }
                QMessageBox QPushButton:hover { background-color: #403e3b; color: #ffffff; }
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
                QPushButton#booked:hover { background-color: #8B1A10; color: #888888; }
                QPushButton#activeTab { font-size: 12px; background-color: #e0e0e0; color: #000000; border-radius: 0px; padding: 10px 5px; font-weight: bold; border-bottom: 3px solid #629924; }
                QPushButton#inactiveTab { font-size: 12px; background-color: transparent; color: #888888; border-radius: 0px; padding: 10px 5px; font-weight: bold; }
                QPushButton#inactiveTab:hover { background-color: #f5f5f5; color: #555555; }
                QMessageBox { background-color: #ffffff; }
                QMessageBox QLabel { background-color: transparent; color: #2b2b2b; font-size: 14px; font-weight: normal; }
                QMessageBox QPushButton { background-color: #edebe9; color: #2b2b2b; border-radius: 3px; padding: 8px 15px; min-width: 80px; font-size: 13px; }
                QMessageBox QPushButton:hover { background-color: #dcdad8; }
            """)
            self.theme_btn.setIcon(QIcon(self.dark_mode))
        
    def update_halls(self,live_data):
        self.last_live_data = live_data
        halls = sorted(live_data.keys())
        for hall_id in halls:
            periods_data = live_data[hall_id]
            status = periods_data.get(self.current_period, 'unknown')
            if hall_id not in self.hall_buttons:
                btn = QPushButton()
                btn.setFixedSize(QSize(234,133))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                self.hall_buttons[hall_id] = btn
                
                btn.setEnabled(True)
                btn.clicked.connect(partial(self.hall_clicked, hall_id))
                
                count = len(self.hall_buttons) - 1
                row = count // 3
                col = count % 3
                self.grid_layout.addWidget(btn, row, col)
            
            btn = self.hall_buttons[hall_id]
            if status == "available":
                btn.setObjectName("available")
                btn.setText(f"{hall_id}\nAvailable")
            else:
                btn.setObjectName("booked")
                btn.setText(f"{hall_id}\nBooked")
        self.apply_theme()
        
    def hall_clicked(self, hall_id):
        btn = self.hall_buttons[hall_id]
        if btn.objectName() == "available":
            self._confirm_booking(hall_id)
        elif btn.objectName() == "booked":
            self._confirm_unbooking(hall_id)
    def _confirm_booking(self, hall_id):
        reply = QMessageBox.question(
            self, "Confirm Booking",
            f"Do you want to book {hall_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.book_hall(hall_id, self.current_period)
            if not success:
                QMessageBox.critical(self, "Booking Failed", msg)
    def _confirm_unbooking(self, hall_id):
        reply = QMessageBox.question(
            self, "Confirm Unbooking",
            f"Do you want to unbook {hall_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db_manager.unbook_hall(hall_id, self.current_period)
            if not success:
                QMessageBox.critical(self, "Unbooking Failed", msg)

    def switch_period(self, selected_period):
        if self.current_period == selected_period:
            return
        self.current_period = selected_period
        for period, btn in self.tab_buttons.items():
            if period == self.current_period:
                btn.setObjectName("activeTab")
            else:
                btn.setObjectName("inactiveTab")
        self.apply_theme()
        if self.last_live_data:
            self.update_halls(self.last_live_data)

if __name__ == "__main__":
    app = QApplication([])
    window = HallBookingUI()
    window.show()
    sys.exit(app.exec())