# Display/Elements/TyreDisplay.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PySide6.QtCore import Qt, Slot, QRectF

class TyreWidget(QWidget):
    def __init__(self, position, parent=None):
        super().__init__(parent)
        self.position = position  # FL, FR, RL, RR
        self.temperature = 25.0
        self.pressure = 12.0
        self.setFixedSize(40, 60)

    def get_color_for_temp(self):
        """Retorna cor baseada na temperatura"""
        if self.temperature < 40:
            return QColor("#00BFFF")  # Azul - Frio
        elif self.temperature < 70:
            return QColor("#39FF14")  # Verde - Ideal
        elif self.temperature < 90:
            return QColor("#FFD700")  # Amarelo - Quente
        else:
            return QColor("#FF073A")  # Vermelho - Muito quente

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Desenhar pneu como retângulo arredondado
        rect = self.rect().adjusted(2, 2, -2, -2)
        color = self.get_color_for_temp()
        
        painter.setPen(QPen(color.darker(150), 2))
        painter.setBrush(QBrush(color))
        painter.drawRoundedRect(rect, 8, 8)
        
        # Desenhar detalhes do pneu (linhas)
        painter.setPen(QPen(QColor("#000000"), 1))
        for i in range(1, 4):
            y = rect.height() * i / 4
            painter.drawLine(rect.left() + 4, y, rect.right() - 4, y)

    def update_data(self, temp, pressure):
        self.temperature = temp
        self.pressure = pressure
        self.update()

class TyreDisplayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 180)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border: 1px solid #555555;
                border-radius: 10px;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)
        
        # Título
        title = QLabel("PNEUS")
        title.setFont(QFont("Arial", 10, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Criar widgets dos pneus
        self.tyres = {
            'FL': TyreWidget('FL'),  # Front Left
            'FR': TyreWidget('FR'),  # Front Right
            'RL': TyreWidget('RL'),  # Rear Left
            'RR': TyreWidget('RR')   # Rear Right
        }
        
        # Layout do carro (vista de cima)
        car_layout = QVBoxLayout()
        car_layout.setSpacing(15)
        
        # Pneus dianteiros
        front_layout = QHBoxLayout()
        front_layout.addWidget(self.tyres['FL'])
        front_layout.addStretch()
        front_layout.addWidget(self.tyres['FR'])
        
        # Desenho simplificado do carro
        car_body = QWidget()
        car_body.setFixedSize(60, 40)
        car_body.setStyleSheet("""
            background-color: #444444;
            border: 1px solid #666666;
            border-radius: 5px;
        """)
        car_center = QHBoxLayout()
        car_center.addStretch()
        car_center.addWidget(car_body)
        car_center.addStretch()
        
        # Pneus traseiros
        rear_layout = QHBoxLayout()
        rear_layout.addWidget(self.tyres['RL'])
        rear_layout.addStretch()
        rear_layout.addWidget(self.tyres['RR'])
        
        car_layout.addLayout(front_layout)
        car_layout.addLayout(car_center)
        car_layout.addLayout(rear_layout)
        
        main_layout.addLayout(car_layout)
        
        # Legenda de temperatura
        legend_layout = QHBoxLayout()
        legend_layout.setSpacing(5)
        
        colors_temps = [
            ("#00BFFF", "FRIO"),
            ("#39FF14", "IDEAL"), 
            ("#FFD700", "QUENTE"),
            ("#FF073A", "CRÍTICO")
        ]
        
        for color, text in colors_temps:
            color_box = QWidget()
            color_box.setFixedSize(10, 10)
            color_box.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
            
            label = QLabel(text)
            label.setFont(QFont("Arial", 6))
            label.setStyleSheet("color: #AAAAAA; background: transparent;")
            
            legend_layout.addWidget(color_box)
            legend_layout.addWidget(label)
        
        main_layout.addLayout(legend_layout)
        main_layout.addStretch()

    @Slot(dict)
    def updateTyreData(self, tyre_data):
        """
        Atualiza dados dos pneus
        tyre_data = {
            'FL': {'temp': 45.5, 'pressure': 12.3},
            'FR': {'temp': 47.2, 'pressure': 12.1},
            'RL': {'temp': 43.8, 'pressure': 12.4},
            'RR': {'temp': 46.1, 'pressure': 12.2}
        }
        """
        for position, data in tyre_data.items():
            if position in self.tyres:
                self.tyres[position].update_data(
                    data['temp'], 
                    data['pressure']
                )