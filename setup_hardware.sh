#!/data/data/com.termux/files/usr/bin/bash
# HormigasAIS — Setup Hardware en Termux
echo "[SETUP] Instalando dependencias hardware..."

pkg update -y
pkg install -y python python-pip usbutils

# pyserial para comunicacion con ESP8266
pip install pyserial --break-system-packages

echo "[SETUP] Verificando puerto USB..."
ls /dev/ttyUSB* 2>/dev/null || echo "[AVISO] Conecta el ESP8266 y recarga"

echo "[SETUP] Permisos de puerto serial..."
# En Termux con root:
# chmod 666 /dev/ttyUSB0
# Sin root: usar Termux:API o solicitar permiso via Android

echo "[SETUP] Listo. Flujo de arranque:"
echo "  1. Flashear firmware_esp8266.ino al ESP via Arduino IDE"
echo "  2. Conectar ESP8266 via OTG USB al A16"
echo "  3. python3 colonia_bus_hw.py"
