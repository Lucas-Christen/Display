# data/simulators/RaceDataSimulator.py
from PySide6.QtCore import QObject, Signal, QTimer
import time

class RaceDataSimulator(QObject):
    lap_data_updated = Signal(dict)

    def __init__(self, update_frequency_hz=10):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._generate_data)
        self.update_interval_ms = int(1000 / update_frequency_hz)

        self.best_lap = [0, 0, 0]
        self.previous_lap = [0, 0, 0]
        self.current_lap = [0, 0, 0]
        self.current_sector = 0
        self.sector_start_time = 0

    def _format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        ms = int((seconds * 1000) % 1000)
        return f"{mins:02d}:{secs:02d}.{ms:03d}"
    
    def _generate_data(self):
        elapsed_time = time.time() - self.sector_start_time
        self.current_lap[self.current_sector] = elapsed_time

        # Simula a passagem de setor
        if elapsed_time > 25 + (self.current_sector * 5): # Duração de setor progressiva
            self.sector_start_time = time.time()
            self.current_sector += 1
            if self.current_sector > 2: # Completou a volta
                self.current_sector = 0
                self.previous_lap = self.current_lap[:]
                
                total_lap_time = sum(self.previous_lap)
                if sum(self.best_lap) == 0 or total_lap_time < sum(self.best_lap):
                    self.best_lap = self.previous_lap[:]
                
                self.current_lap = [0, 0, 0]

        data = {
            "best": [self._format_time(t) for t in self.best_lap],
            "previous": [self._format_time(t) for t in self.previous_lap],
            "current": [self._format_time(t) for t in self.current_lap]
        }
        self.lap_data_updated.emit(data)

    def start(self):
        self.sector_start_time = time.time()
        self.timer.start(self.update_interval_ms)

    def stop(self):
        self.timer.stop()