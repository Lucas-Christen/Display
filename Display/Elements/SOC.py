# Display/Elements/SOC.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient
from PySide6.QtCore import Qt, Slot

class SocBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0.0
        self.setMinimumHeight(35) # Garante que o widget nunca desapareça

    @Slot(float)
    def setValue(self, value):
        self._value = max(0.0, min(1.0, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(1,1,-1,-1)
        painter.setPen(QPen(QColor("#555555"), 2))
        painter.setBrush(QColor("#1A1A1A"))
        painter.drawRoundedRect(rect, 8, 8)
        
        num_segments, spacing = 20, 3
        total_spacing = spacing * (num_segments - 1)
        segment_width = (rect.width() - 10 - total_spacing) / num_segments
        if segment_width <= 0: return

        painter.setPen(Qt.NoPen)
        filled_segments = int(self._value * num_segments)
        for i in range(filled_segments):
            x_pos = 5 + i * (segment_width + spacing)
            segment_rect = self.rect().adjusted(x_pos, 5, -(rect.width() - x_pos - segment_width), -5)
            
            gradient = QLinearGradient(segment_rect.topLeft(), segment_rect.bottomLeft())
            gradient.setColorAt(0, QColor("#FFC300"))
            gradient.setColorAt(1, QColor("#FFA500"))
            painter.setBrush(gradient)
            painter.drawRoundedRect(segment_rect, 4, 4)