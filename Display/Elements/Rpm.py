# Display/Elements/Rpm.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient
from PySide6.QtCore import Qt, Slot, QPointF

class RpmIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rpm = 0
        self.max_rpm = 10000
        self.green_color = QColor("#39FF14")
        self.blue_color = QColor("#00BFFF")
        self.setMinimumHeight(40) # Garante que o widget nunca desapareça

    @Slot(int)
    def setRpm(self, rpm):
        self._rpm = rpm
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.width() <= 0 or self.height() <= 0: return

        num_leds = 18
        leds_to_light = int((self._rpm / self.max_rpm) * num_leds)
        led_diameter = min(self.height() * 0.9, self.width() / num_leds)
        if led_diameter <= 0: return

        spacing = (self.width() - num_leds * led_diameter) / (num_leds - 1) if num_leds > 1 else 0

        for i in range(num_leds):
            x = i * (led_diameter + spacing)
            y = (self.height() - led_diameter) / 2
            base_color = self.green_color if i < 12 else self.blue_color
            
            if i < leds_to_light:
                gradient = QLinearGradient(QPointF(x, y), QPointF(x, y + led_diameter))
                gradient.setColorAt(0, base_color.lighter(130))
                gradient.setColorAt(1, base_color)
                painter.setBrush(gradient)
            else:
                painter.setBrush(QColor("#333333"))
            
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x, y, led_diameter, led_diameter)

class DigitalRpm(QWidget):
    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self.value_label = QLabel("0")
        self.unit_label = QLabel("RPM")
        
        self.value_label.setFont(QFont(font_family, 48, QFont.Bold))
        self.unit_label.setFont(QFont(font_family, 18))
        self.value_label.setStyleSheet("color: #FFFFFF; border: none; background: transparent;")
        self.unit_label.setStyleSheet("color: #AAAAAA; border: none; background: transparent;")
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(-5) # Espaçamento negativo para aproximar
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)

    @Slot(int)
    def setValue(self, rpm):
        self.value_label.setText(f"{rpm}")