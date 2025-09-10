# Display/Grid/Layouts.py
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

class DashboardLayout:
    def __init__(self, parent_widget, font_family):
        self.layout = QGridLayout(parent_widget)
        self.font_family = font_family
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(25, 20, 25, 20)

        # Define a proporção das colunas e linhas para o novo layout
        # 6 colunas: Tyre Display | Lap Times | Velocímetro (2 cols) | Temps | Pedals | Fail Alerts  
        self.layout.setColumnStretch(0, 2)  # Tyre Display
        self.layout.setColumnStretch(1, 3)  # Lap Times  
        self.layout.setColumnStretch(2, 3)  # Velocímetro (parte 1)
        self.layout.setColumnStretch(3, 3)  # Velocímetro (parte 2)
        self.layout.setColumnStretch(4, 2)  # Temperaturas
        self.layout.setColumnStretch(5, 2)  # Pedais
        
        # 6 linhas: RPM | RPM Digital | Widgets principais | Continuação | Fail Alerts | SOC
        self.layout.setRowStretch(0, 1)  # RPM Leds
        self.layout.setRowStretch(1, 1)  # RPM Digital
        self.layout.setRowStretch(2, 4)  # Widgets principais (linha 1)
        self.layout.setRowStretch(3, 4)  # Widgets principais (linha 2)
        self.layout.setRowStretch(4, 2)  # Fail Alerts
        self.layout.setRowStretch(5, 1)  # SOC Bar

    def add_element(self, widget, row, col, row_span=1, col_span=1, alignment=Qt.AlignmentFlag.AlignCenter):
        """Adiciona um widget ao grid com spans e alinhamento."""
        self.layout.addWidget(widget, row, col, row_span, col_span, alignment)

    def create_and_add_label(self, text, row, col, text_color, row_span=1, col_span=1, alignment=Qt.AlignmentFlag.AlignLeft, font_size=12):
        """
        Cria e adiciona um QLabel com estilo customizado.
        """
        label = QLabel(text)
        label.setFont(QFont(self.font_family, font_size))
        
        # Converte QColor para string hexadecimal
        if isinstance(text_color, QColor):
            color_str = text_color.name()
        else:
            color_str = text_color
            
        label.setStyleSheet(f"color: {color_str}; background-color: transparent;")
        
        self.layout.addWidget(label, row, col, row_span, col_span, alignment)
        return label