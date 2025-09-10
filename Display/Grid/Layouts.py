# Display/Grid/Layouts.py (CORRIGIDO)
from PySide6.QtWidgets import QGridLayout, QLabel
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

class DashboardLayout:
    def __init__(self, parent_widget, font_family):
        self.layout = QGridLayout(parent_widget)
        self.font_family = font_family
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(25, 20, 25, 20)

        # Define a proporção das colunas e linhas
        self.layout.setColumnStretch(0, 2) # Margem esquerda e Label Velocímetro
        self.layout.setColumnStretch(1, 4) # Conteúdo principal (RPM Digital, Velocímetro)
        self.layout.setColumnStretch(2, 2) # Temp Container
        self.layout.setColumnStretch(3, 2) # Pedal Widget
        self.layout.setColumnStretch(4, 2) # Margem direita e Label RPM

        self.layout.setRowStretch(0, 2) # RPM Leds
        self.layout.setRowStretch(1, 2) # RPM Digital + Labels superiores
        self.layout.setRowStretch(2, 5) # Velocímetro e Gauges
        self.layout.setRowStretch(3, 1) # Espaçamento
        self.layout.setRowStretch(4, 1) # SOC Bar
        self.layout.setRowStretch(5, 1) # Label SOC

    def add_element(self, widget, row, col, row_span=1, col_span=1, alignment=Qt.AlignmentFlag.AlignCenter):
        """Adiciona um widget ao grid com spans e alinhamento."""
        self.layout.addWidget(widget, row, col, row_span, col_span, alignment)

    def create_and_add_label(self, text, row, col, text_color, row_span=1, col_span=1, alignment=Qt.AlignmentFlag.AlignLeft, font_size=12):
        """
        Cria e adiciona um QLabel com estilo customizado.
        Esta é a correção principal: garante que a cor seja tratada corretamente.
        """
        label = QLabel(text)
        label.setFont(QFont(self.font_family, font_size))
        
        # A CORREÇÃO CRÍTICA:
        # Usamos .name() para garantir que o objeto QColor seja convertido para uma string (ex: "#AAAAAA")
        label.setStyleSheet(f"color: {text_color.name()}; background-color: transparent;")
        
        self.layout.addWidget(label, row, col, row_span, col_span, alignment)
        return label