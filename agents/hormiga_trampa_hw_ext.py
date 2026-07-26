# EXTENSION para hormiga_trampa.py — agregar metodo activar_gpio()
# Conectar segundo ESP8266 (o mismo via segundo canal) que controle:
#   D1 -> Relay Resistencia IR
#   D2 -> Relay Ventilador
#   D3 -> LED UV (ya activo en firmware, este lo modula)

import serial, json, time

PUERTO_TRAMPA = "/dev/ttyUSB1"  # Si hay segundo ESP; si es uno solo, mismo puerto
BAUD_TRAMPA   = 115200

class GPIOBridge:
    def __init__(self):
        self.ser = None
        self._conectar()

    def _conectar(self):
        try:
            self.ser = serial.Serial(PUERTO_TRAMPA, BAUD_TRAMPA, timeout=1)
            print(f"[HW-TRAMPA] GPIO Bridge activo en {PUERTO_TRAMPA}")
        except Exception as e:
            print(f"[HW-TRAMPA] Sin GPIO Bridge: {e} — modo simulacion activo")
            self.ser = None

    def _enviar(self, cmd):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write((json.dumps(cmd) + "\n").encode())
            except Exception as e:
                print(f"[HW-TRAMPA] Error GPIO: {e}")

    def activar_trampa(self, intensidad):
        potencia = 100 if intensidad > 0.85 else 60
        self._enviar({
            "cmd": "trampa_on",
            "ir_on": True,
            "fan_pct": potencia,
            "uv_on": True
        })

    def apagar_trampa(self):
        self._enviar({
            "cmd": "trampa_off",
            "ir_on": False,
            "fan_pct": 0,
            "uv_on": True  # UV siempre activo para atraccion pasiva
        })

    def cerrar(self):
        if self.ser:
            self.apagar_trampa()
            time.sleep(0.5)
            self.ser.close()

# Instrucciones de integracion:
# 1. En HormigaTrampa.__init__() agregar: self.gpio = GPIOBridge()
# 2. En reaccionar() agregar:             self.gpio.activar_trampa(intensidad)
# 3. En apagado_seguro() agregar:         self.gpio.apagar_trampa()
