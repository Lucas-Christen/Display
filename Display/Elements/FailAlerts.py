# Display/Elements/FailAlerts.py
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Slot, QTimer
import random

class FailAlertsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 160)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border: 1px solid #555555;
                border-radius: 10px;
            }
        """)
        
        layout = QGridLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        title_label = QLabel("SISTEMAS")
        title_label.setFont(QFont("Arial", 10, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label, 0, 0, 1, 2)
        
        # Criar indicadores para cada sistema
        self.systems = {
            'motor': self.create_system_indicator("⚡", "MOTOR"),
            'battery': self.create_system_indicator("🔋", "BATERIA"),
            'inverter': self.create_system_indicator("🔌", "INVERSOR"),
            'bms': self.create_system_indicator("🖥️", "BMS")
        }
        
        # Organizar em grid 2x2
        layout.addWidget(self.systems['motor'], 1, 0)
        layout.addWidget(self.systems['battery'], 1, 1)
        layout.addWidget(self.systems['inverter'], 2, 0)
        layout.addWidget(self.systems['bms'], 2, 1)
        
        # Timer para simular falhas aleatórias (apenas para demonstração)
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.simulate_system_status)
        self.simulation_timer.start(3000)  # Atualiza a cada 3 segundos

    def create_system_indicator(self, icon, name):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 100, 0, 100);
                border: 1px solid #39FF14;
                border-radius: 8px;
            }
        """)
        
        from PySide6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 20px; background: transparent; border: none;")
        icon_label.setAlignment(Qt.AlignCenter)
        
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 8, QFont.Bold))
        name_label.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        name_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        
        widget.is_error = False  # Estado do sistema
        return widget

    def set_system_status(self, system_name, is_error):
        """Define o status de um sistema (True = erro, False = ok)"""
        if system_name in self.systems:
            widget = self.systems[system_name]
            widget.is_error = is_error
            
            if is_error:
                widget.setStyleSheet("""
                    QWidget {
                        background-color: rgba(255, 7, 58, 150);
                        border: 2px solid #FF073A;
                        border-radius: 8px;
                    }
                """)
            else:
                widget.setStyleSheet("""
                    QWidget {
                        background-color: rgba(0, 100, 0, 100);
                        border: 1px solid #39FF14;
                        border-radius: 8px;
                    }
                """)

    def simulate_system_status(self):
        """Simula falhas aleatórias para demonstração"""
        for system in self.systems.keys():
            # 10% de chance de erro em cada sistema
            has_error = random.random() < 0.1
            self.set_system_status(system, has_error)

    @Slot(dict)
    def update_system_status(self, status_dict):
        """Atualiza o status dos sistemas baseado em dados reais"""
        for system, is_error in status_dict.items():
            self.set_system_status(system, is_error)