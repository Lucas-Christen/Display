# Display/Elements/Rpm.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient, QRadialGradient, QBrush
from PySide6.QtCore import Qt, Slot, QPointF

class RpmIndicator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rpm = 0
        self.max_rpm = 10000
        self.green_color = QColor("#39FF14")
        self.orange_color = QColor("#FF8C00")  
        self.blue_color = QColor("#1E90FF")
        self.setMinimumHeight(120)  # Aumentado para dar mais espaço aos efeitos 3D
        self.setMaximumHeight(140)
        
        # Cores para efeitos 3D
        self.led_off_color = QColor("#1A1A1A")
        self.led_border_color = QColor("#333333")

    @Slot(int)
    def setRpm(self, rpm):
        self._rpm = max(0, min(self.max_rpm, rpm))
        self.update()

    def get_led_colors(self, led_index, total_leds):
        """Retorna as cores para cada LED baseado na sua posição"""
        # Dividir em 3 zonas: Verde (0-4), Laranja (5-9), Azul (10-14)
        if led_index < 5:  # Zona Verde (0-33%)
            base_color = self.green_color
        elif led_index < 10:  # Zona Laranja (33-66%)
            base_color = self.orange_color
        else:  # Zona Azul (66-100%)
            base_color = self.blue_color
        
        # Cores para efeito 3D
        highlight = QColor(base_color.lighter(160))
        shadow = QColor(base_color.darker(140))
        
        return base_color, highlight, shadow

    def create_radial_gradient(self, center, radius, base_color, highlight, shadow, is_lit=True):
        """Cria um gradiente radial para efeito 3D"""
        gradient = QRadialGradient(center, radius)
        
        if is_lit:
            # LED aceso - efeito brilhante
            gradient.setColorAt(0.0, highlight)
            gradient.setColorAt(0.3, base_color)
            gradient.setColorAt(0.7, base_color.darker(110))
            gradient.setColorAt(1.0, shadow)
        else:
            # LED apagado - efeito fosco
            gradient.setColorAt(0.0, QColor("#2A2A2A"))
            gradient.setColorAt(0.3, self.led_off_color)
            gradient.setColorAt(0.7, self.led_off_color.darker(120))
            gradient.setColorAt(1.0, QColor("#0A0A0A"))
        
        return gradient

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        if rect.width() <= 0 or rect.height() <= 0:
            return

        # Configurações dos LEDs
        num_leds = 15
        margin = 40  # Margem maior para LEDs maiores
        available_width = rect.width() - (2 * margin)
        
        if available_width <= 0:
            return
        
        # Calcular tamanho dos LEDs
        spacing = 8  # Espaçamento fixo entre LEDs
        total_spacing = spacing * (num_leds - 1)
        led_diameter = min(50, (available_width - total_spacing) / num_leds)
        
        if led_diameter < 15:
            led_diameter = 15  # Tamanho mínimo para boa visualização
            spacing = max(2, (available_width - (num_leds * led_diameter)) / (num_leds - 1))
        
        # Calcular quantos LEDs devem estar acesos
        rpm_percentage = self._rpm / self.max_rpm
        leds_to_light = int(rpm_percentage * num_leds)
        
        # Desenhar fundo da barra (opcional - trilho dos LEDs)
        painter.setBrush(QBrush(QColor("#0F0F0F")))
        painter.setPen(Qt.NoPen)
        track_rect = rect.adjusted(margin - 10, rect.height() // 2 - 8, -margin + 10, rect.height() // 2 + 8)
        painter.drawRoundedRect(track_rect, 8, 8)
        
        painter.setPen(Qt.NoPen)
        
        # Desenhar cada LED
        for i in range(num_leds):
            # Calcular posição do centro do LED
            x_center = margin + (led_diameter / 2) + i * (led_diameter + spacing)
            y_center = rect.height() / 2
            center_point = QPointF(x_center, y_center)
            
            # Obter cores para este LED
            base_color, highlight, shadow = self.get_led_colors(i, num_leds)
            
            # Determinar se o LED está aceso
            is_lit = i < leds_to_light
            
            # Criar gradiente radial para efeito 3D
            radius = led_diameter / 2
            gradient = self.create_radial_gradient(center_point, radius, base_color, highlight, shadow, is_lit)
            
            # Desenhar o LED principal
            painter.setBrush(QBrush(gradient))
            led_rect = QPointF(x_center - radius, y_center - radius)
            painter.drawEllipse(led_rect.x(), led_rect.y(), led_diameter, led_diameter)
            
            # Adicionar brilho extra para LEDs acesos
            if is_lit:
                # Highlight no topo do LED
                highlight_gradient = QRadialGradient(
                    QPointF(x_center - radius * 0.3, y_center - radius * 0.3), 
                    radius * 0.4
                )
                highlight_gradient.setColorAt(0.0, QColor(255, 255, 255, 100))
                highlight_gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
                
                painter.setBrush(QBrush(highlight_gradient))
                highlight_size = led_diameter * 0.6
                painter.drawEllipse(
                    x_center - highlight_size / 2, 
                    y_center - highlight_size / 2, 
                    highlight_size, 
                    highlight_size
                )
                
                # Efeito de glow ao redor do LED
                if rpm_percentage > 0.8:  # Glow extra em RPMs altos
                    glow_gradient = QRadialGradient(center_point, radius * 1.8)
                    glow_color = QColor(base_color)
                    glow_color.setAlpha(30)
                    glow_gradient.setColorAt(0.0, glow_color)
                    glow_gradient.setColorAt(1.0, QColor(base_color.red(), base_color.green(), base_color.blue(), 0))
                    
                    painter.setBrush(QBrush(glow_gradient))
                    glow_size = led_diameter * 2.2
                    painter.drawEllipse(
                        x_center - glow_size / 2, 
                        y_center - glow_size / 2, 
                        glow_size, 
                        glow_size
                    )

        # Adicionar indicadores de zona (opcional)
        self.draw_zone_indicators(painter, rect, margin, led_diameter, spacing, num_leds)

    def draw_zone_indicators(self, painter, rect, margin, led_diameter, spacing, num_leds):
        """Desenha pequenos indicadores das zonas de RPM"""
        painter.setPen(QColor("#666666"))
        painter.setBrush(Qt.NoBrush)
        
        # Posições das divisões das zonas (LED 5 e LED 10)
        zone_positions = [5, 10]
        
        for zone_led in zone_positions:
            if zone_led < num_leds:
                x_pos = margin + (led_diameter / 2) + zone_led * (led_diameter + spacing) - spacing / 2
                # Pequena linha vertical indicando mudança de zona
                painter.drawLine(
                    x_pos, rect.height() / 2 - led_diameter / 2 - 5,
                    x_pos, rect.height() / 2 + led_diameter / 2 + 5
                )

class DigitalRpm(QWidget):
    def __init__(self, font_family=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 120)
        
        # Debug: Verificar se a fonte foi carregada
        print(f"[DigitalRpm] Font family recebida: {font_family}")
        
        # Usar fonte padrão se não foi fornecida ou falhou
        if font_family is None or font_family == "" or font_family == "Consolas":
            print("[DigitalRpm] AVISO: Usando fonte padrão Arial")
            self.font_family = "Arial"
        else:
            self.font_family = font_family
            print(f"[DigitalRpm] Usando fonte: {self.font_family}")
        
        # Estilo da caixa com bordas douradas
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, 
                                                   stop:0 rgba(60, 60, 60, 255), 
                                                   stop:1 rgba(40, 40, 40, 255));
                border: 3px solid #FFD700; 
                border-radius: 12px;
            }
        """)
        
        # Criar labels
        self.value_label = QLabel("0")
        self.unit_label = QLabel("RPM")
        
        # Aplicar fontes com tratamento de erro
        try:
            value_font = QFont(self.font_family, 54, QFont.Bold)
            unit_font = QFont(self.font_family, 18, QFont.Bold)
            
            # Verificar se a fonte foi aplicada corretamente
            if value_font.family() != self.font_family:
                print(f"[DigitalRpm] AVISO: Fonte {self.font_family} não disponível, usando {value_font.family()}")
            
            self.value_label.setFont(value_font)
            self.unit_label.setFont(unit_font)
            
        except Exception as e:
            print(f"[DigitalRpm] ERRO ao aplicar fonte: {e}")
            # Fallback para fonte padrão
            self.value_label.setFont(QFont("Arial", 54, QFont.Bold))
            self.unit_label.setFont(QFont("Arial", 18, QFont.Bold))
        
        # Cores douradas
        self.value_label.setStyleSheet("color: #FFD700; border: none; background: transparent;")
        self.unit_label.setStyleSheet("color: #FFA500; border: none; background: transparent;")
        
        self.value_label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.unit_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(-8)
        layout.addWidget(self.value_label)
        layout.addWidget(self.unit_label)
        
        print(f"[DigitalRpm] Widget inicializado com sucesso")

    @Slot(int)
    def setValue(self, rpm):
        try:
            self.value_label.setText(f"{rpm}")
        except Exception as e:
            print(f"[DigitalRpm] ERRO ao definir RPM {rpm}: {e}")
            # Fallback simples
            self.value_label.setText("ERR")