# data/simulators/PedalSimulator.py

from PySide6.QtCore import QObject, Signal, QTimer
import random

class PedalSimulator(QObject):
    """
    Simula a pressão no acelerador e no freio.
    Alterna entre estados de aceleração e frenagem.
    """
    pressure_updated = Signal(int, int) # (acelerador, freio)

    def __init__(self, update_frequency_hz=20):
        super().__init__()
        self._accelerator = 0
        self._brake = 0
        self._state = "accelerating" # Pode ser 'accelerating' ou 'braking'
        self._state_duration = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._generate_data)
        self.update_interval_ms = int(1000 / update_frequency_hz)

    def _generate_data(self):
        if self._state_duration <= 0:
            # Troca de estado
            if self._state == "accelerating":
                self._state = "braking"
                self._state_duration = random.randint(10, 30) # Dura de 0.5s a 1.5s freando
            else:
                self._state = "accelerating"
                self._state_duration = random.randint(50, 150) # Dura de 2.5s a 7.5s acelerando
        
        if self._state == "accelerating":
            self._accelerator = random.randint(70, 100)
            self._brake = 0
        else:
            self._accelerator = 0
            self._brake = random.randint(60, 100)
            
        self._state_duration -= 1
        
        # Emite os sinais
        self.pressure_updated.emit(self._accelerator, self._brake)

    def start(self):
        self._state_duration = random.randint(50, 150) # Duração inicial
        self.timer.start(self.update_interval_ms)

    def stop(self):
        self.timer.stop()