# Display/Elements/LapsIndicators.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Slot

class LapTimesWidget(QWidget):
    def __init__(self, font_family, parent=None):
        super().__init__(parent)
        self.font_family = font_family
        self.setMinimumSize(200, 180)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 180);
                border: 1px solid #555555;
                border-radius: 10px;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Melhor Volta
        best_label = QLabel("MELHOR VOLTA")
        best_label.setFont(QFont(font_family, 10, QFont.Bold))
        best_label.setStyleSheet("color: #39FF14; background: transparent;")
        best_label.setAlignment(Qt.AlignCenter)
        
        self.best_sectors = self.create_sector_row("00:00.000", "00:00.000", "00:00.000")
        
        # Volta Anterior
        prev_label = QLabel("VOLTA ANTERIOR")
        prev_label.setFont(QFont(font_family, 10, QFont.Bold))
        prev_label.setStyleSheet("color: #FFD700; background: transparent;")
        prev_label.setAlignment(Qt.AlignCenter)
        
        self.prev_sectors = self.create_sector_row("00:00.000", "00:00.000", "00:00.000")
        
        # Volta Atual
        current_label = QLabel("VOLTA ATUAL")
        current_label.setFont(QFont(font_family, 10, QFont.Bold))
        current_label.setStyleSheet("color: #00BFFF; background: transparent;")
        current_label.setAlignment(Qt.AlignCenter)
        
        self.current_sectors = self.create_sector_row("00:00.000", "00:00.000", "00:00.000")
        
        # Adicionar todos ao layout
        main_layout.addWidget(best_label)
        main_layout.addLayout(self.best_sectors)
        main_layout.addWidget(prev_label)
        main_layout.addLayout(self.prev_sectors)
        main_layout.addWidget(current_label)
        main_layout.addLayout(self.current_sectors)
        main_layout.addStretch()

    def create_sector_row(self, s1_time, s2_time, s3_time):
        layout = QHBoxLayout()
        layout.setSpacing(5)
        
        sectors = []
        for i, time in enumerate([s1_time, s2_time, s3_time], 1):
            sector_label = QLabel(f"S{i}")
            sector_label.setFont(QFont(self.font_family, 8))
            sector_label.setStyleSheet("color: #AAAAAA; background: transparent;")
            sector_label.setAlignment(Qt.AlignCenter)
            
            time_label = QLabel(time)
            time_label.setFont(QFont(self.font_family, 9, QFont.Bold))
            time_label.setStyleSheet("color: #FFFFFF; background: transparent;")
            time_label.setAlignment(Qt.AlignCenter)
            
            sector_widget = QWidget()
            sector_layout = QVBoxLayout(sector_widget)
            sector_layout.setContentsMargins(2, 2, 2, 2)
            sector_layout.setSpacing(1)
            sector_layout.addWidget(sector_label)
            sector_layout.addWidget(time_label)
            
            layout.addWidget(sector_widget)
            sectors.append(time_label)
        
        # Armazenar referências para atualização
        if not hasattr(self, 'sector_labels'):
            self.sector_labels = {}
        
        return layout

    @Slot(dict)
    def update_lap_times(self, lap_data):
        """
        Atualiza os tempos com dados do simulador
        lap_data = {
            "best": ["00:25.123", "00:23.456", "00:27.890"],
            "previous": ["00:26.123", "00:24.456", "00:28.890"],
            "current": ["00:15.123", "00:00.000", "00:00.000"]
        }
        """
        # Este método será chamado pelo DataAggregator quando implementado
        pass