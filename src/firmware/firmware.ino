#include <OneWire.h>
#include <DallasTemperature.h>

const byte SENSOR_PIN = 2;
const unsigned long READ_INTERVAL_MS = 1000;

OneWire oneWire(SENSOR_PIN);
DallasTemperature sensor(&oneWire);

unsigned long lastReadingTime = 0;

void setup() {
  Serial.begin(9600);
  sensor.begin();
  sensor.setResolution(12);

  Serial.println("uptime_ms,temperature_c");
}

void loop() {
  unsigned long now = millis();

  if (now - lastReadingTime < READ_INTERVAL_MS) {
    return;
  }
  lastReadingTime = now;

  sensor.requestTemperatures();
  float temperatureC = sensor.getTempCByIndex(0);

  if (temperatureC == DEVICE_DISCONNECTED_C) {
    Serial.println("# Sensor missing or read failed");
    return;
  }

  Serial.print(millis());
  Serial.print(',');
  Serial.println(temperatureC, 2);
}
