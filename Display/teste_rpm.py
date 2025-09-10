# teste_rpm.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer
# Importamos diretamente o RpmIndicator do seu ficheiro existente
from Display.Elements.Rpm import RpmIndicator

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teste do RpmIndicator")
        self.setGeometry(100, 100, 800, 200)

        # 1. Criamos uma instância do seu RpmIndicator
        self.rpm_widget = RpmIndicator(self)
        self.setCentralWidget(self.rpm_widget)

        # 2. Um timer para simular a mudança de RPM e ver a animação
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rpm)
        self.timer.start(50) # Atualiza a cada 50ms
        self.current_rpm = 0
        self.direction = 1

    def update_rpm(self):
        # Lógica simples para fazer o RPM subir e descer
        self.current_rpm += 200 * self.direction
        if self.current_rpm >= self.rpm_widget.max_rpm or self.current_rpm <= 0:
            self.direction *= -1
        
        # 3. Chamamos o método setRpm para atualizar o widget
        self.rpm_widget.setRpm(self.current_rpm)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())