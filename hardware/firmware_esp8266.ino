// HormigasAIS — Firmware Centinela Hardware v1.0
// ESP8266 NodeMCU + PIR HC-SR501
// Envia JSON al puerto Serial (115200) -> Termux lee /dev/ttyUSB0

#include <Arduino.h>
#include <ArduinoJson.h>

#define PIN_PIR     D5   // HC-SR501 OUT -> D5
#define PIN_LED_UV  D6   // LED UV -> D6 (atraccion nocturna)
#define UMBRAL_MS   2000 // Debounce: ignorar re-triggers < 2s

const char* NODE_ID  = "centinela_hw_01";
const char* VERSION  = "1.0.0-hw";
unsigned long ultimo_trigger = 0;
bool uv_activo = false;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PIR,    INPUT);
  pinMode(PIN_LED_UV, OUTPUT);
  // UV siempre encendido en modo nocturno (atraccion pasiva)
  digitalWrite(PIN_LED_UV, HIGH);
  uv_activo = true;
  Serial.println("{"boot":"HormigasAIS-HW","node":"" + 
                 String(NODE_ID) + ""}");
}

void loop() {
  int pir_estado = digitalRead(PIN_PIR);
  unsigned long ahora = millis();

  if (pir_estado == HIGH && (ahora - ultimo_trigger) > UMBRAL_MS) {
    ultimo_trigger = ahora;

    // Leer pin analogico como proxy de intensidad termica
    // En hardware real: reemplazar con sensor MLX90614 I2C
    float intensidad = 0.75 + (analogRead(A0) / 1023.0) * 0.25;

    StaticJsonDocument<200> doc;
    doc["timestamp"] = ahora / 1000.0;
    doc["type"]      = "mosquito_pulse";
    doc["origin"]    = NODE_ID;
    doc["status"]    = "active";
    doc["intensity"] = intensidad;
    doc["hw"]        = true;

    // Emitir al bus serial -> Termux
    serializeJson(doc, Serial);
    Serial.println();  // flush de linea
  }

  delay(100);
}
