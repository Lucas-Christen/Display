# Display/Elements/Rpm.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient, QRadialGradient, QBrush
from PySide6.QtCore import Qt, Slot, QPointF

class RpmIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rpm = 0
        self.max_rpm = 10000
        self.green_color = QColor("#39FF14")
        self.orange_color = QColor("#FF8C00")  
        self.blue_color = QColor("#1E90FF")
        self.setMinimumHeight(80)
        self.setMaximumHeight(100)

    @Slot(int)
    def setRpm(self, rpm):
        self._rpm = rpm
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        if rect.width() <= 0 or rect.height() <= 0:
            return

        # Configurações das bolinhas
        num_leds = 15
        margin = 30
        available_width = rect.width() - (2 * margin)
        
        if available_width <= 0:
            return
            
        led_diameter = min(40, available_width / num_leds * 0.8)
        if led_diameter <= 5:
            led_diameter = 20  # Tamanho mínimo
            
        # Calcular quantos LEDs devem estar acesos
        leds_to_light = int((self._rpm / self.max_rpm) * num_leds)
        
        # Calcular espaçamento
        total_leds_width = num_leds * led_diameter
        if total_leds_width < available_width:
            spacing = (available_width - total_leds_width) / (num_leds + 1)
        else:
            spacing = 2
            led_diameter = (available_width - (spacing * (num_leds + 1))) / num_leds

        painter.setPen(Qt.NoPen)
        
        for i in range(num_leds):
            # Posição da bolinha
            x = margin + spacing + i * (led_diameter + spacing)
            y = (rect.height() - led_diameter) / 2
            
            # Definir cor baseada na posição
            if i < 5:  # Primeiros 5: Verde
                color = self.green_color
            elif i < 10:  # Próximos 5: Laranja
                color = self.orange_color
            else:  # Últimos 5: Azul
                color = self.blue_color
            
            # Desenhar a bolinha
            if i < leds_to_light:
                # LED aceso - usar cor vibrante
                painter.setBrush(QBrush(color))
            else:
                # LED apagado - usar cor escura
                painter.setBrush(QBrush(QColor("#333333")))
            
            # Desenhar círculo
            painter.drawEllipse(int(x), int(y), int(led_diameter), int(led_diameter))

class DigitalRpm(QWidget):
    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 120)  # Aumentado para números maiores
        
        # Estilo da caixa com bordas douradas como na imagem
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                                   stop:0 rgba(60, 60, 60, 255), 
                                                   stop:1 rgba(40, 40, 40, 255));
                border: 3px solid #FFD700; 
                border-radius: 12px;
            }
        """)
        
        self.value_label = QLabel("0")
        self.unit_label = QLabel("RPM")
        
        # Fontes muito maiores para melhor visibilidade
        self.value_label.setFont(QFont(font_family, 54, QFont.Bold))  # Aumentado
        self.unit_label.setFont(QFont(font_family, 18, QFont.Bold))
        
        # Cores douradas como na imagem
        self.value_label.setStyleSheet("color: #FFD700; border: none; background: transparent;")
        self.unit_label.setStyleSheet("color: #FFA500; border: none; background: transparent;")
        
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(-8)
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)

    @Slot(int)
    def setValue(self, rpm):
        self.value_label.setText(f"{rpm}")