# Display/Elements/SOC.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QFont
from PySide6.QtCore import Qt, Slot
import random

class SocBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0.98
        self._power_flow = 0.0  # kW/h - negativo = descarga, positivo = recarga
        self.setMinimumHeight(80)
        
        # Label para mostrar o fluxo de potência
        self.power_label = QLabel("0.0 kW/h")
        self.power_label.setStyleSheet("color: #FFFFFF; background: transparent; font-weight: bold;")
        self.power_label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addStretch()
        layout.addWidget(self.power_label)

    @Slot(float)
    def setValue(self, value):
        self._value = max(0.0, min(1.0, value))
        # Simular fluxo de potência baseado no SOC
        self._power_flow = random.uniform(-5.5, 2.0)  # Mais descarga que recarga
        self.update_power_display()
        self.update()

    def update_power_display(self):
        if self._power_flow < 0:
            self.power_label.setText(f"{self._power_flow:.1f} kW/h")
            self.power_label.setStyleSheet("color: #FF073A; background: transparent; font-weight: bold;")
        else:
            self.power_label.setText(f"+{self._power_flow:.1f} kW/h")
            self.power_label.setStyleSheet("color: #39FF14; background: transparent; font-weight: bold;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Área para a barra (deixa espaço para o label)
        bar_rect = self.rect().adjusted(1, 1, -1, -30)
        
        # Desenhar fundo da barra
        painter.setPen(QPen(QColor("#555555"), 2))
        painter.setBrush(QColor("#1A1A1A"))
        painter.drawRoundedRect(bar_rect, 10, 10)
        
        num_segments = 10  # Dividido em 10 segmentos
        spacing = 4
        total_spacing = spacing * (num_segments - 1)
        segment_width = (bar_rect.width() - 20 - total_spacing) / num_segments
        if segment_width <= 0: return

        painter.setPen(Qt.NoPen)
        filled_segments = int(self._value * num_segments)
        
        for i in range(filled_segments):
            x_pos = 10 + i * (segment_width + spacing)
            segment_rect = bar_rect.adjusted(x_pos, 8, -(bar_rect.width() - x_pos - segment_width), -8)
            
            # Cor do segmento baseada no nível
            if i < 3:  # Vermelho para baixo nível
                color1, color2 = QColor("#FF073A"), QColor("#CC0000")
            elif i < 6:  # Amarelo para nível médio
                color1, color2 = QColor("#FFD700"), QColor("#FFA500")
            else:  # Verde para nível alto
                color1, color2 = QColor("#39FF14"), QColor("#00CC00")
            
            gradient = QLinearGradient(segment_rect.topLeft(), segment_rect.bottomLeft())
            gradient.setColorAt(0, color1)
            gradient.setColorAt(1, color2)
            painter.setBrush(gradient)
            painter.drawRoundedRect(segment_rect, 3, 3)