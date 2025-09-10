# teste_completo.py
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QFontDatabase, QFont, QColor, QPalette
from PySide6.QtCore import QTimer, Qt

# Tentar importar os componentes
try:
    from Display.Elements.Rpm import RpmIndicator, DigitalRpm
    print("✅ Importação dos componentes RPM bem-sucedida")
except ImportError as e:
    print(f"❌ ERRO na importação: {e}")
    sys.exit(1)

class DiagnosticWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diagnóstico Completo - RPM Display")
        self.setGeometry(100, 100, 1000, 400)
        
        # Configurar fundo escuro como no sistema principal
        self.setStyleSheet("background-color: #101010;")
        
        print("\n🔧 INICIANDO DIAGNÓSTICO...")
        
        # 1. Testar carregamento da fonte
        self.test_font_loading()
        
        # 2. Criar o layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 3. Criar widgets de teste
        self.create_test_widgets(main_layout)
        
        # 4. Timer para simular RPM
        self.setup_rpm_simulation()
        
    def test_font_loading(self):
        """Testa o carregamento da fonte Orbitron"""
        print("\n📝 TESTANDO CARREGAMENTO DE FONTE...")
        
        # Verificar se o arquivo existe
        font_path = "Display/assets/fonts/Orbitron-Bold.ttf"
        if not os.path.exists(font_path):
            print(f"❌ Arquivo de fonte não encontrado: {font_path}")
            print(f"   Diretório atual: {os.getcwd()}")
            print(f"   Conteúdo do diretório Display/assets/fonts/:")
            try:
                if os.path.exists("Display/assets/fonts/"):
                    files = os.listdir("Display/assets/fonts/")
                    for file in files:
                        print(f"     - {file}")
                else:
                    print("     Diretório não existe!")
            except:
                print("     Erro ao listar diretório")
            
            self.font_family = "Arial"  # Fallback
            return
        
        # Tentar carregar a fonte
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            self.font_family = families[0] if families else "Arial"
            print(f"✅ Fonte carregada com sucesso: {self.font_family}")
            print(f"   Famílias disponíveis: {families}")
        else:
            print(f"❌ Falha ao carregar a fonte: {font_path}")
            self.font_family = "Arial"
        
    def create_test_widgets(self, main_layout):
        """Cria os widgets de teste"""
        print("\n🎛️ CRIANDO WIDGETS DE TESTE...")
        
        # Título
        title = QLabel("TESTE DE DIAGNÓSTICO - RPM INDICATOR")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #FFFFFF; margin: 10px;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Container para os widgets RPM
        rpm_container = QWidget()
        rpm_layout = QVBoxLayout(rpm_container)
        rpm_layout.setSpacing(15)
        
        # Tentar criar RpmIndicator
        try:
            print("  🔄 Criando RpmIndicator...")
            self.rpm_indicator = RpmIndicator()
            rpm_layout.addWidget(self.rpm_indicator)
            print("  ✅ RpmIndicator criado com sucesso")
        except Exception as e:
            print(f"  ❌ ERRO ao criar RpmIndicator: {e}")
            self.rpm_indicator = None
            
        # Tentar criar DigitalRpm
        try:
            print(f"  🔄 Criando DigitalRpm com fonte: {self.font_family}")
            self.digital_rpm = DigitalRpm(self.font_family)
            
            # Container centralizado para o RPM digital
            digital_container = QWidget()
            digital_layout = QHBoxLayout(digital_container)
            digital_layout.addStretch()
            digital_layout.addWidget(self.digital_rpm)
            digital_layout.addStretch()
            
            rpm_layout.addWidget(digital_container)
            print("  ✅ DigitalRpm criado com sucesso")
        except Exception as e:
            print(f"  ❌ ERRO ao criar DigitalRpm: {e}")
            import traceback
            traceback.print_exc()
            self.digital_rpm = None
            
        main_layout.addWidget(rpm_container)
        
        # Informações de diagnóstico
        info_label = QLabel(f"Fonte carregada: {self.font_family}")
        info_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(info_label)
        
    def setup_rpm_simulation(self):
        """Configura a simulação de RPM"""
        print("\n⏱️ CONFIGURANDO SIMULAÇÃO DE RPM...")
        
        self.current_rpm = 0
        self.direction = 1
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rpm)
        self.timer.start(100)  # Atualiza a cada 100ms
        
        print("  ✅ Simulação iniciada")
        
    def update_rpm(self):
        """Atualiza o RPM simulado"""
        try:
            # Aumentar/diminuir RPM
            self.current_rpm += 150 * self.direction
            
            # Inverter direção nos limites
            if self.current_rpm >= 10000:
                self.current_rpm = 10000
                self.direction = -1
            elif self.current_rpm <= 0:
                self.current_rpm = 0
                self.direction = 1
                
            # Atualizar widgets
            if self.rpm_indicator:
                self.rpm_indicator.setRpm(self.current_rpm)
                
            if self.digital_rpm:
                self.digital_rpm.setValue(self.current_rpm)
                
        except Exception as e:
            print(f"❌ ERRO na simulação RPM: {e}")

if __name__ == "__main__":
    print("🚀 INICIANDO TESTE DE DIAGNÓSTICO...")
    
    app = QApplication(sys.argv)
    
    try:
        window = DiagnosticWindow()
        window.show()
        print("\n✅ JANELA CRIADA - Verificar se ambos os widgets aparecem")
        print("   - Bolinhas coloridas (RpmIndicator)")
        print("   - Número digital com bordas douradas (DigitalRpm)")
        print("\n🎯 Se apenas as bolinhas aparecerem, o problema está no DigitalRpm")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"\n💥 ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()