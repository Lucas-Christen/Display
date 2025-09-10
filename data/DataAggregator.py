# data/DataAggregator.py

from PySide6.QtCore import QObject, Signal

from data.simulators.EngineSimulator import EngineSimulator
from data.simulators.BatterySimulator import BatterySimulator
from data.simulators.PedalSimulator import PedalSimulator
from data.simulators.TyresSimulator import TyresSimulator
from data.simulators.RaceDataSimulator import RaceDataSimulator

class DataAggregator(QObject):
    """
    Agrega todos os simuladores de dados em uma única interface com sinais unificados
    para a camada de Display.
    """
    # Sinais para o Front-End
    new_rpm_value = Signal(int)
    new_speed_value = Signal(int)
    new_engine_temp_value = Signal(float)
    new_soc_value = Signal(float)
    new_battery_temp_value = Signal(float)
    new_pedal_pressure_values = Signal(int, int)  # (accelerator, brake)
    new_tyre_data = Signal(dict)
    new_lap_data = Signal(dict)  # Dados de volta
    new_system_status = Signal(dict)  # Status dos sistemas

    def __init__(self):
        super().__init__()
        # Instancia todos os simuladores com suas frequências
        self.engine_sim = EngineSimulator(update_frequency_hz=50)
        self.battery_sim = BatterySimulator(update_frequency_hz=2)
        self.pedal_sim = PedalSimulator(update_frequency_hz=20)
        self.tyre_sim = TyresSimulator(update_frequency_hz=1)
        self.race_sim = RaceDataSimulator(update_frequency_hz=10)

        # Conecta os sinais de cada simulador aos sinais unificados deste agregador
        self.engine_sim.rpm_updated.connect(self.new_rpm_value)
        self.engine_sim.speed_updated.connect(self.new_speed_value)
        self.engine_sim.temp_updated.connect(self.new_engine_temp_value)
        
        self.battery_sim.soc_updated.connect(self.new_soc_value)
        self.battery_sim.temp_updated.connect(self.new_battery_temp_value)

        self.pedal_sim.pressure_updated.connect(self.new_pedal_pressure_values)
        
        self.tyre_sim.tyre_data_updated.connect(self.new_tyre_data)
        
        self.race_sim.lap_data_updated.connect(self.new_lap_data)

    def start_all_simulators(self):
        """Inicia todos os timers de simulação."""
        self.engine_sim.start()
        self.battery_sim.start()
        self.pedal_sim.start()
        self.tyre_sim.start()
        self.race_sim.start()

    def stop_all_simulators(self):
        """Para todos os timers de simulação."""
        self.engine_sim.stop()
        self.battery_sim.stop()
        self.pedal_sim.stop()
        self.tyre_sim.stop()
        self.race_sim.stop()