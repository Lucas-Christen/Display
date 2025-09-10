# data/simulators/TyresSimulator.py

from PySide6.QtCore import QObject, Signal, QTimer
import random

class TyresSimulator(QObject):
    """
    Simula temperatura e pressão para os 4 pneus (FL, FR, RL, RR).
    Envia os dados em um dicionário. Frequência baixa.
    """
    tyre_data_updated = Signal(dict)

    def __init__(self, update_frequency_hz=2):
        super().__init__()
        # Estrutura de dados para os 4 pneus
        self.tyre_data = {
            'FL': {'temp': 25.0, 'pressure': 12.0},
            'FR': {'temp': 25.0, 'pressure': 12.0},
            'RL': {'temp': 25.0, 'pressure': 12.0},
            'RR': {'temp': 25.0, 'pressure': 12.0},
        }

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._generate_data)
        self.update_interval_ms = int(1000 / update_frequency_hz)

    def _generate_data(self):
        # Simula o aquecimento dos pneus durante uma volta
        for tyre in self.tyre_data:
            # Aumenta a temperatura até um limite operacional
            current_temp = self.tyre_data[tyre]['temp']
            if current_temp < 95.0:
                self.tyre_data[tyre]['temp'] += random.uniform(0.1, 0.5)

            # A pressão aumenta com a temperatura (relação simplificada)
            current_pressure = self.tyre_data[tyre]['pressure']
            if current_pressure < 15.0:
                 self.tyre_data[tyre]['pressure'] += random.uniform(0.01, 0.05)

        self.tyre_data_updated.emit(self.tyre_data)

    def start(self):
        self.timer.start(self.update_interval_ms)

    def stop(self):
        self.timer.stop()