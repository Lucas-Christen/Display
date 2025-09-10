# Display/Elements/Speed.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot

class SpeedWidget(QWidget):
    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                                   stop:0 rgba(45, 45, 45, 255), 
                                                   stop:1 rgba(30, 30, 30, 255));
                border: 2px solid #555555; 
                border-radius: 15px;
            }
        """)
        
        self.value_label = QLabel("0")
        self.unit_label = QLabel("KM/H")
        
        self.value_label.setFont(QFont(font_family, 90, QFont.Bold))
        self.unit_label.setFont(QFont(font_family, 30))
        self.value_label.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        self.unit_label.setStyleSheet("color: #AAAAAA; background: transparent; border: none;")
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(-15)
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)
        
    @Slot(int)
    def setValue(self, speed):
        self.value_label.setText(f"{speed}")