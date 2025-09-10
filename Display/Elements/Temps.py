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
        self.icon_type = icon_type  # "battery" ou "motor"
        self.setMinimumSize(60, 150)
        
        # Label para mostrar o valor numérico
        self.value_label = QLabel(f"{vmin}°C")
        self.value_label.setStyleSheet("color: #FFFFFF; background: transparent; font-weight: bold;")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        # Label para o ícone/tipo
        self.icon_label = QLabel("🔋" if icon_type == "battery" else "🔥")
        self.icon_label.setStyleSheet("font-size: 20px; background: transparent;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self.icon_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    @Slot(float)
    def setValue(self, value):
        self._value = max(self.min_val, min(self.max_val, value))
        self.value_label.setText(f"{self._value:.0f}°C")
        self.update()

    def get_color_for_temperature(self):
        """Retorna a cor baseada na temperatura"""
        percentage = (self._value - self.min_val) / (self.max_val - self.min_val)
        
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
        bar_rect = self.rect().adjusted(8, 30, -8, -25)
        
        # Desenhar fundo
        painter.setPen(QPen(QColor("#555555"), 2))
        painter.setBrush(QColor("#1A1A1A"))
        painter.drawRoundedRect(bar_rect, 8, 8)

        if (self.max_val - self.min_val) == 0: return
        
        # Calcular altura do preenchimento
        fill_percentage = (self._value - self.min_val) / (self.max_val - self.min_val)
        fill_height = fill_percentage * bar_rect.height()
        fill_rect = QRectF(bar_rect.x() + 2, bar_rect.y() + bar_rect.height() - fill_height, 
                          bar_rect.width() - 4, fill_height)
        
        # Cor dinâmica baseada na temperatura
        temp_color = self.get_color_for_temperature()
        gradient = QLinearGradient(fill_rect.topLeft(), fill_rect.bottomLeft())
        gradient.setColorAt(0, temp_color.lighter(130))
        gradient.setColorAt(1, temp_color)
        
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(fill_rect, 6, 6)