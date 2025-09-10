# data/simulators/EngineSimulator.py

from PySide6.QtCore import QObject, Signal, QTimer
import random

class EngineSimulator(QObject):
    """
    Simula dados do motor (RPM, Velocidade, Temperatura).
    RPM e Velocidade são atualizados em alta frequência.
    """
    rpm_updated = Signal(int)
    speed_updated = Signal(int)
    temp_updated = Signal(float)

    def __init__(self, update_frequency_hz=50):
        super().__init__()
        self._rpm = 0
        self._speed = 0
        self._temp = 75.0  # Temperatura inicial
        self._rpm_direction = 1 # 1 para subir, -1 para descer

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._generate_data)
        self.update_interval_ms = int(1000 / update_frequency_hz)

    def _generate_data(self):
        # 1. Simula o RPM em um padrão de "dente de serra" para parecer um piloto acelerando e trocando de marcha
        if self._rpm_direction == 1:
            self._rpm += random.randint(150, 200)
            if self._rpm > 9500:
                self._rpm = 8000 # Simula troca de marcha
                self._rpm_direction = random.choice([-1, 1]) # Às vezes continua subindo
        else:
            self._rpm -= random.randint(250, 300)
            if self._rpm < 2000:
                self._rpm = 2000
                self._rpm_direction = 1

        # 2. Calcula a velocidade baseada no RPM (relação simples)
        self._speed = int((self._rpm / 9500) * 130) + random.randint(-2, 2)
        if self._speed < 0: self._speed = 0

        # 3. Simula a temperatura do motor
        # Aquece mais rápido em RPMs altos, esfria lentamente em RPMs baixos
        if self._rpm > 6000:
            self._temp += 0.05
        else:
            self._temp -= 0.03
        
        # Mantém a temperatura dentro de limites
        self._temp = max(70.0, min(115.0, self._temp))

        # Emite os sinais
        self.rpm_updated.emit(self._rpm)
        self.speed_updated.emit(self._speed)
        self.temp_updated.emit(round(self._temp, 2))

    def start(self):
        self.timer.start(self.update_interval_ms)

    def stop(self):
        self.timer.stop()