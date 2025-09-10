# Display/Elements/Speed.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot

class SpeedWidget(QWidget):
    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 160)  # Maior para números grandes
        
        # Estilo similar ao RPM mas com bordas azuis
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                                   stop:0 rgba(60, 60, 60, 255), 
                                                   stop:1 rgba(40, 40, 40, 255));
                border: 3px solid #00BFFF; 
                border-radius: 15px;
            }
        """)
        
        self.value_label = QLabel("0")
        self.unit_label = QLabel("KM/H")
        
        # Fontes muito maiores como na imagem
        self.value_label.setFont(QFont(font_family, 72, QFont.Bold))  # Bem grande
        self.unit_label.setFont(QFont(font_family, 20, QFont.Bold))
        
        # Cores ciano/azul como na imagem
        self.value_label.setStyleSheet("color: #00FFFF; background: transparent; border: none;")
        self.unit_label.setStyleSheet("color: #00BFFF; background: transparent; border: none;")
        
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(-12)
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)
        
    @Slot(int)
    def setValue(self, speed):
        self.value_label.setText(f"{speed}")