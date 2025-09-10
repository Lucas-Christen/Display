# Display/Elements/PedalPressure.py
from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Slot
from .Temps import VerticalBarGauge

class PedalPressureWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0,0,0,0)
        
        # Corrigido: usar a nova assinatura da VerticalBarGauge
        self.accelerator_bar = VerticalBarGauge("#00FF00", 0, 100, "accelerator")
        self.brake_bar = VerticalBarGauge("#FF0000", 0, 100, "brake")
        
        layout.addWidget(self.accelerator_bar)
        layout.addWidget(self.brake_bar)

    @Slot(int, int)
    def update_pressures(self, accelerator, brake):
        self.accelerator_bar.setValue(accelerator)
        self.brake_bar.setValue(brake)