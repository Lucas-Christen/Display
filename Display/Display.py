# Display/Display.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QPalette, QFontDatabase, QFont
from PySide6.QtCore import Qt

# Importa todas as nossas classes
from data.DataAggregator import DataAggregator
from Display.Grid.Layouts import DashboardLayout
from Display.Elements.Rpm import RpmIndicator, DigitalRpm
from Display.Elements.Speed import SpeedWidget
from Display.Elements.SOC import SocBar
from Display.Elements.Temps import VerticalBarGauge
from Display.Elements.PedalPressure import PedalPressureWidget
from Display.Elements.LapsIndicators import LapTimesWidget
from Display.Elements.FailAlerts import FailAlertsWidget
from Display.Elements.TyreDisplay import TyreDisplayWidget

class MainDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard F-Elétrico")
        self.setGeometry(50, 50, 1366, 768)

        # Paleta de Cores
        self.COLOR_BACKGROUND = QColor("#101010")
        self.COLOR_RPM_GREEN = QColor("#39FF14")
        self.COLOR_RPM_YELLOW = QColor("#FFD700")
        self.COLOR_RPM_RED = QColor("#FF073A")
        self.COLOR_ACCELERATOR = self.COLOR_RPM_GREEN
        self.COLOR_BRAKE = QColor("#FF073A")
        self.COLOR_BATT_TEMP = QColor("#FFA500")
        self.COLOR_MOTOR_TEMP = QColor("#FF4500")
        self.COLOR_TEXT_PRIMARY = QColor("#FFFFFF")
        self.COLOR_TEXT_SECONDARY = QColor("#AAAAAA")
        
        palette = self.palette()
        palette.setColor(QPalette.Window, self.COLOR_BACKGROUND)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Carregamento da Fonte
        font_id = QFontDatabase.addApplicationFont("Display/assets/fonts/Orbitron-Bold.ttf")
        if font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("AVISO: Fonte 'Orbitron-Bold.ttf' não encontrada.")
            self.font_family = "Consolas"

        self.data_aggregator = DataAggregator()

        # Criar os widgets da UI, passando a fonte
        self.rpm_indicator = RpmIndicator()
        self.digital_rpm = DigitalRpm(self.font_family)
        self.speed_widget = SpeedWidget(self.font_family)
        self.soc_bar = SocBar()
        self.battery_temp_gauge = VerticalBarGauge(self.COLOR_BATT_TEMP, 0, 80, "battery")
        self.engine_temp_gauge = VerticalBarGauge(self.COLOR_MOTOR_TEMP, 0, 50, "motor")
        self.pedal_widget = PedalPressureWidget()
        self.lap_times_widget = LapTimesWidget(self.font_family)
        self.fail_alerts_widget = FailAlertsWidget()
        self.tyre_display_widget = TyreDisplayWidget()
        
        # Aplicando Cores e Efeitos
        self.rpm_indicator.green_color = self.COLOR_RPM_GREEN
        self.rpm_indicator.yellow_color = self.COLOR_RPM_YELLOW
        self.rpm_indicator.red_color = self.COLOR_RPM_RED
        self.pedal_widget.accelerator_bar.color = self.COLOR_ACCELERATOR
        self.pedal_widget.brake_bar.color = self.COLOR_BRAKE
        
        glow_effect = lambda color, radius=25: QGraphicsDropShadowEffect(blurRadius=radius, color=color, offset=0)
        self.speed_widget.setGraphicsEffect(glow_effect(self.COLOR_BATT_TEMP))
        self.digital_rpm.setGraphicsEffect(glow_effect(self.COLOR_TEXT_PRIMARY, radius=20))

        # Conectar sinais aos slots
        self.data_aggregator.new_rpm_value.connect(self.rpm_indicator.setRpm)
        self.data_aggregator.new_rpm_value.connect(self.digital_rpm.setValue)
        self.data_aggregator.new_speed_value.connect(self.speed_widget.setValue)
        self.data_aggregator.new_soc_value.connect(self.soc_bar.setValue)
        self.data_aggregator.new_battery_temp_value.connect(self.battery_temp_gauge.setValue)
        self.data_aggregator.new_engine_temp_value.connect(self.engine_temp_gauge.setValue)
        self.data_aggregator.new_pedal_pressure_values.connect(self.pedal_widget.update_pressures)
        self.data_aggregator.new_tyre_data.connect(self.tyre_display_widget.updateTyreData)
        
        # Configurar o Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout_manager = DashboardLayout(central_widget, self.font_family)
        
        # Container para temperaturas
        temp_container = QWidget()
        temp_layout = QHBoxLayout(temp_container)
        temp_layout.setSpacing(15)
        temp_layout.setContentsMargins(0,0,0,0)
        temp_layout.addWidget(self.battery_temp_gauge)
        temp_layout.addWidget(self.engine_temp_gauge)

        # Layout principal - 6 colunas x 6 linhas
        # Linha 0: RPM Indicator (ocupa toda a largura)
        layout_manager.add_element(self.rpm_indicator, 0, 0, 1, 6)
        
        # Linha 1: RPM Digital (centro)
        layout_manager.add_element(self.digital_rpm, 1, 2, 1, 2, Qt.AlignCenter)
        
        # Linha 2: Tyre Display | Lap Times | Velocímetro | Temperaturas | Pedais | Fail Alerts
        layout_manager.add_element(self.tyre_display_widget, 2, 0, 2, 1, Qt.AlignCenter)
        layout_manager.add_element(self.lap_times_widget, 2, 1, 2, 1, Qt.AlignCenter)
        layout_manager.add_element(self.speed_widget, 2, 2, 2, 2, Qt.AlignCenter)
        layout_manager.add_element(temp_container, 2, 4, 2, 1, Qt.AlignCenter)
        layout_manager.add_element(self.pedal_widget, 2, 5, 2, 1, Qt.AlignCenter)
        
        # Linha 4: Fail Alerts (esquerda inferior)
        layout_manager.add_element(self.fail_alerts_widget, 4, 0, 2, 1, Qt.AlignCenter)
        
        # Linha 5: SOC Bar (ocupa largura central)
        layout_manager.add_element(self.soc_bar, 5, 1, 1, 4, Qt.AlignVCenter)

        self.data_aggregator.start_all_simulators()
        
    def closeEvent(self, event):
        self.data_aggregator.stop_all_simulators()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainDisplay()
    window.show()
    sys.exit(app.exec())