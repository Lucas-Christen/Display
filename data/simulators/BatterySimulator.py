# data/simulators/BatterySimulator.py

from PySide6.QtCore import QObject, Signal, QTimer
import random

class BatterySimulator(QObject):
    """
    Simula o estado da carga (SOC) e a temperatura do pack de baterias.
    Atualiza em uma frequência mais baixa.
    """
    soc_updated = Signal(float)
    temp_updated = Signal(float)

    def __init__(self, update_frequency_hz=2):
        super().__init__()
        self._soc = 0.98  # Começa com 98%
        self._temp = 28.0 # Temperatura inicial

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._generate_data)
        self.update_interval_ms = int(1000 / update_frequency_hz)

    def _generate_data(self):
        # 1. Simula o consumo da bateria (SOC)
        # O consumo é maior em picos aleatórios (simulando alta demanda de potência)
        consumo = random.uniform(0.0001, 0.0005)
        self._soc -= consumo
        if self._soc < 0:
            self._soc = 1.0 # Reinicia a simulação

        # 2. Simula a temperatura da bateria
        # A temperatura sobe um pouco com o uso e se dissipa lentamente
        self._temp += random.uniform(-0.1, 0.2)
        self._temp = max(25.0, min(65.0, self._temp)) # Limites de segurança

        # Emite os sinais
        self.soc_updated.emit(round(self._soc, 4))
        self.temp_updated.emit(round(self._temp, 2))

    def start(self):
        self.timer.start(self.update_interval_ms)

    def stop(self):
        self.timer.stop()