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
        self.yellow_color = QColor("#FFD700")  
        self.red_color = QColor("#FF073A")
        self.setMinimumHeight(60)

    @Slot(int)
    def setRpm(self, rpm):
        self._rpm = rpm
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self.width() <= 0 or self.height() <= 0: return

        num_leds = 30  # Mais LEDs para melhor resolução
        leds_to_light = int((self._rpm / self.max_rpm) * num_leds)
        led_diameter = min(self.height() * 0.8, self.width() / num_leds * 0.9)
        if led_diameter <= 0: return

        spacing = (self.width() - num_leds * led_diameter) / (num_leds + 1)

        for i in range(num_leds):
            x = spacing + i * (led_diameter + spacing)
            y = (self.height() - led_diameter) / 2
            
            # Definir cor baseada na posição
            if i < 18:  # 60% verde (0-6000 RPM)
                base_color = self.green_color
            elif i < 24:  # 20% amarelo (6000-8000 RPM)
                base_color = self.yellow_color
            else:  # 20% vermelho (8000-10000 RPM)
                base_color = self.red_color
            
            if i < leds_to_light:
                gradient = QLinearGradient(QPointF(x, y), QPointF(x, y + led_diameter))
                gradient.setColorAt(0, base_color.lighter(150))
                gradient.setColorAt(0.5, base_color)
                gradient.setColorAt(1, base_color.darker(120))
                painter.setBrush(gradient)
            else:
                painter.setBrush(QColor("#333333"))
            
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(x, y, led_diameter, led_diameter)

class DigitalRpm(QWidget):
    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 100)  # Tamanho fixo para caixa RPM
        
        # Estilo da caixa
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                                   stop:0 rgba(45, 45, 45, 255), 
                                                   stop:1 rgba(30, 30, 30, 255));
                border: 2px solid #555555; 
                border-radius: 10px;
            }
        """)
        
        self.value_label = QLabel("0")
        self.unit_label = QLabel("RPM")
        
        # Fonte maior para até 4 dígitos
        self.value_label.setFont(QFont(font_family, 32, QFont.Bold))
        self.unit_label.setFont(QFont(font_family, 14))
        self.value_label.setStyleSheet("color: #FFFFFF; border: none; background: transparent;")
        self.unit_label.setStyleSheet("color: #AAAAAA; border: none; background: transparent;")
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(-5)
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)

    @Slot(int)
    def setValue(self, rpm):
        self.value_label.setText(f"{rpm}")