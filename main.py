import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGridLayout)
from PyQt6.QtCore import Qt

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

        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.setObjectName("themeBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFixedWidth(120)
        
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_btn)
        self.layout.addLayout(header_layout)
        
        #hall booking in a grid layout
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        #mock data for halls
        self.halls = ['501', '502', '503', '504', '508', '509', '511', '512', '515', '518']
        self.hall_buttons = {}
        
        self.build_grid()
        self.apply_themeai()
        self.layout.addStretch()
        
    def build_grid(self):
        row, col = 0, 0
        for hall in self.halls:
            btn = QPushButton(f"Hall {hall}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            if hall == '502':
                btn.setObjectName("booked")
                btn.setText(f"Hall {hall}\n(Booked)")
            else:
                btn.setObjectName("available")
                btn.setText(f"Hall {hall}\n(Available)")
            self.grid_layout.addWidget(btn, row, col)
            self.hall_buttons[hall] = btn
            col+=1
            if col == 3:
                col = 0
                row += 1
            
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_themeai()
    def apply_theme(self):
        if not self.is_dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                    color: #333;
                }
                QPushButton#themeBtn {
                    background-color: #333;
                    color: #fff;
                }
                QLabel#titleText {
                    font-size: 24px;
                    font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #333;
                    color: #f0f0f0;
                }
                QPushButton#themeBtn {
                    background-color: #f0f0f0;
                    color: #333;
                }
                QLabel#titleText {
                    font-size: 24px;
                    font-weight: bold;
                }
            """)
    def apply_themeai(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #161512; color: #bababa; font-family: Arial; }
                QLabel#titleText { font-size: 22px; font-weight: bold; color: #ffffff; }
                QPushButton { border: none; border-radius: 4px; padding: 20px; font-weight: bold; font-size: 14px; }
                QPushButton#themeBtn { background-color: #262421; color: #bababa; padding: 10px; }
                QPushButton#themeBtn:hover { background-color: #363431; color: #ffffff; }
                QPushButton#available { background-color: #629924; color: white; }
                QPushButton#available:hover { background-color: #72a934; }
                QPushButton#booked { background-color: #302e2b; color: #666666; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #edebe9; color: #2b2b2b; font-family: Arial; }
                QLabel#titleText { font-size: 22px; font-weight: bold; color: #2b2b2b; }
                QPushButton { border: none; border-radius: 4px; padding: 20px; font-weight: bold; font-size: 14px; }
                QPushButton#themeBtn { background-color: #ffffff; color: #2b2b2b; padding: 10px; }
                QPushButton#themeBtn:hover { background-color: #e0e0e0; }
                QPushButton#available { background-color: #7fb041; color: white; }
                QPushButton#available:hover { background-color: #8fc051; }
                QPushButton#booked { background-color: #cccccc; color: #888888; }
            """)
        
if __name__ == "__main__":
    app = QApplication([])
    window = HallBookingUI()
    window.show()
    sys.exit(app.exec())