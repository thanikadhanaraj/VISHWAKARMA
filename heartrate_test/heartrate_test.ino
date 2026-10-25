
#include <Wire.h>
#include "MAX30105.h"

MAX30105 sensor;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(21, 22);
  Wire.setClock(100000);

  Serial.println();
  Serial.println("MAX30102 RAW IR TEST");

  if (!sensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("ERROR: Sensor not found!");
    Serial.println("Check VIN, GND, SDA, and SCL.");
    while (true) {
      delay(1000);
    }
  }

  // Low LED power for an initial signal check
  byte ledBrightness = 0x1F;  // 31/255
  byte sampleAverage = 4;
  byte ledMode = 2;            // Red + IR
  int sampleRate = 100;
  int pulseWidth = 411;
  int adcRange = 4096;

  sensor.setup(
    ledBrightness,
    sampleAverage,
    ledMode,
    sampleRate,
    pulseWidth,
    adcRange
  );

  // Disable the red LED to focus on IR
  sensor.setPulseAmplitudeRed(0);
  sensor.setPulseAmplitudeIR(0x1F);
  sensor.setPulseAmplitudeGreen(0);

  Serial.println("Sensor initialized.");
  Serial.println("Place finger gently over sensor.");
  Serial.println("IR values:");
}

void loop() {
  sensor.check();

  while (sensor.available()) {
    unsigned long ir = sensor.getIR();

    Serial.println(ir);

    sensor.nextSample();
  }
}
