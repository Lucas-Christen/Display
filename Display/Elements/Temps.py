# Display/Elements/Temps.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QLinearGradient
from PySide6.QtCore import Qt, Slot, QRectF

class VerticalBarGauge(QWidget):
    def __init__(self, color, vmin, vmax, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.min_val, self.max_val = vmin, vmax
        self._value = vmin
        self.setMinimumSize(30, 120) # Garante que o widget nunca desapareça

    @Slot(float)
    def setValue(self, value):
        self._value = max(self.min_val, min(self.max_val, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(2, 2, -2, -2)
        
        painter.setPen(QColor("#555555"))
        painter.setBrush(QColor("#1A1A1A"))
        painter.drawRoundedRect(rect, 5, 5)

        if (self.max_val - self.min_val) == 0: return
        fill_percentage = (self._value - self.min_val) / (self.max_val - self.min_val)
        fill_height = fill_percentage * rect.height()
        fill_rect = QRectF(rect.x(), rect.y() + rect.height() - fill_height, rect.width(), fill_height)
        
        gradient = QLinearGradient(fill_rect.topLeft(), fill_rect.bottomLeft())
        gradient.setColorAt(0, self.color.lighter(130))
        gradient.setColorAt(1, self.color)
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(fill_rect)