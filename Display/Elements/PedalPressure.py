# Display/Elements/PedalPressure.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Slot
from .Temps import VerticalBarGauge

class PedalPressureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Container principal
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Usar a nova assinatura da VerticalBarGauge com ícones corretos
        self.accelerator_bar = VerticalBarGauge("#39FF14", 0, 100, "accelerator")
        self.brake_bar = VerticalBarGauge("#FF073A", 0, 100, "brake")
        
        main_layout.addWidget(self.accelerator_bar)
        main_layout.addWidget(self.brake_bar)

    @Slot(int, int)
    def update_pressures(self, accelerator, brake):
        self.accelerator_bar.setValue(accelerator)
        self.brake_bar.setValue(brake)