# Display/Elements/Temps.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QFont, QPen
from PySide6.QtCore import Qt, Slot, QRectF

class VerticalBarGauge(QWidget):
    def __init__(self, default_color, vmin, vmax, icon_type, parent=None):
        super().__init__(parent)
        self.default_color = QColor(default_color)
        self.min_val, self.max_val = vmin, vmax
        self._value = vmin
        self.icon_type = icon_type
        self.setMinimumSize(70, 180)  # Maior para melhor visualização
        
        # Label para mostrar o valor numérico
        self.value_label = QLabel(f"{vmin}°")
        self.value_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.value_label.setStyleSheet("color: #FFFFFF; background: transparent; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        # Ícone correto baseado no tipo (como na imagem)
        if icon_type == "battery":
            self.icon_label = QLabel("🔋")
            self.setStyleSheet("border: 2px solid #FFA500; border-radius: 8px; background: rgba(30,30,30,100);")
        elif icon_type == "motor":
            self.icon_label = QLabel("🔥")
            self.setStyleSheet("border: 2px solid #FF4500; border-radius: 8px; background: rgba(30,30,30,100);")
        elif icon_type == "accelerator":
            self.icon_label = QLabel("⬆")
            self.setStyleSheet("border: 2px solid #39FF14; border-radius: 8px; background: rgba(30,30,30,100);")
        else:  # brake
            self.icon_label = QLabel("⬇")
            self.setStyleSheet("border: 2px solid #FF073A; border-radius: 8px; background: rgba(30,30,30,100);")
            
        self.icon_label.setStyleSheet("font-size: 24px; background: transparent; border: none;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.addWidget(self.icon_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    @Slot(float)
    def setValue(self, value):
        self._value = max(self.min_val, min(self.max_val, value))
        if self.icon_type in ["battery", "motor"]:
            self.value_label.setText(f"{self._value:.0f}°")
        else:
            self.value_label.setText(f"{self._value:.0f}%")
        self.update()

    def get_color_for_temperature(self):
        """Retorna a cor baseada na temperatura"""
        percentage = (self._value - self.min_val) / (self.max_val - self.min_val) if self.max_val != self.min_val else 0
        
        if self.icon_type == "accelerator":
            return QColor("#39FF14")  # Verde sempre para acelerador
        elif self.icon_type == "brake":
            return QColor("#FF073A")  # Vermelho sempre para freio
        
        # Para temperaturas
        if percentage < 0.3:  # Azul - Frio
            return QColor("#00BFFF")
        elif percentage < 0.6:  # Verde - Bom
            return QColor("#39FF14")
        elif percentage < 0.8:  # Amarelo - Preocupante
            return QColor("#FFD700")
        else:  # Vermelho - Emergência
            return QColor("#FF073A")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Área da barra (deixa espaço para ícone e label)
        bar_rect = self.rect().adjusted(12, 35, -12, -30)
        
        # Desenhar fundo
        painter.setPen(QPen(QColor("#555555"), 1))
        painter.setBrush(QColor("#2A2A2A"))
        painter.drawRoundedRect(bar_rect, 6, 6)

        if (self.max_val - self.min_val) == 0: return
        
        # Calcular altura do preenchimento
        fill_percentage = (self._value - self.min_val) / (self.max_val - self.min_val)
        fill_height = fill_percentage * (bar_rect.height() - 4)
        fill_rect = QRectF(bar_rect.x() + 2, bar_rect.y() + bar_rect.height() - fill_height - 2, 
                          bar_rect.width() - 4, fill_height)
        
        # Cor dinâmica baseada na temperatura
        temp_color = self.get_color_for_temperature()
        gradient = QLinearGradient(fill_rect.topLeft(), fill_rect.bottomLeft())
        gradient.setColorAt(0, temp_color.lighter(140))
        gradient.setColorAt(0.5, temp_color)
        gradient.setColorAt(1, temp_color.darker(120))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(fill_rect, 4, 4)