/*
  CARESAFE - ESP32-WROOM-32 + MPU6050 + buzzer threshold demo
  I2C: SDA=GPIO21, SCL=GPIO22
  Buzzer signal: GPIO25

  Prototype only: detects unusually high motion using adjustable thresholds.
  It is NOT a clinically validated fall detector and does not send an emergency alert.
  Test with gentle hand movements / safe simulated movements only. Do not deliberately fall.

  Library needed in Arduino IDE:
    Adafruit MPU6050
    Adafruit Unified Sensor
*/
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

const int SDA_PIN = 21;
const int SCL_PIN = 22;
const int BUZZER_PIN = 25;

// Tune these after observing live serial values.
// Units: acceleration magnitude m/s^2; gyro magnitude rad/s.
const float ACC_THRESHOLD = 22.0;
const float GYRO_THRESHOLD = 3.0;

// Event is flagged when either threshold crosses.
// Cooldown prevents the buzzer from retriggering continuously.
const unsigned long BUZZER_DURATION_MS = 1800;
const unsigned long COOLDOWN_MS = 5000;

unsigned long buzzerOffAt = 0;
unsigned long nextAllowedEventAt = 0;
bool buzzerActive = false;

void startAlert(unsigned long now, float accMag, float gyroMag) {
  Serial.println("!!! DEMO ALERT: CANDIDATE HIGH-MOTION EVENT !!!");
  Serial.print("acc_mag_m_s2=");
  Serial.print(accMag, 2);
  Serial.print(", gyro_mag_rad_s=");
  Serial.println(gyroMag, 2);

  // tone() works for a passive buzzer; an active buzzer can also sound with tone().
  tone(BUZZER_PIN, 2200);
  buzzerActive = true;
  buzzerOffAt = now + BUZZER_DURATION_MS;
  nextAllowedEventAt = now + COOLDOWN_MS;
}

void setup() {
  Serial.begin(115200);
  delay(800);
  pinMode(BUZZER_PIN, OUTPUT);
  noTone(BUZZER_PIN);

  Wire.begin(SDA_PIN, SCL_PIN);
  if (!mpu.begin()) {
    Serial.println("ERROR: MPU6050 not found. Check 3V3, GND, SDA=21, SCL=22.");
    while (true) {
      delay(1000);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  Serial.println("CARESAFE threshold event demo ready.");
  Serial.println("Columns: acc_mag(m/s^2), gyro_mag(rad/s), status");
  Serial.println("Thresholds are prototypes, not validated fall criteria.");
}

void loop() {
  unsigned long now = millis();
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);

  float ax = accel.acceleration.x;
  float ay = accel.acceleration.y;
  float az = accel.acceleration.z;
  float gx = gyro.gyro.x;
  float gy = gyro.gyro.y;
  float gz = gyro.gyro.z;

  float accMag = sqrt(ax * ax + ay * ay + az * az);
  float gyroMag = sqrt(gx * gx + gy * gy + gz * gz);

  bool thresholdCrossed = (accMag >= ACC_THRESHOLD) || (gyroMag >= GYRO_THRESHOLD);

  Serial.print(accMag, 2);
  Serial.print(",");
  Serial.print(gyroMag, 2);
  Serial.print(",");
  Serial.println(thresholdCrossed ? "CANDIDATE_EVENT" : "normal_motion");

  if (buzzerActive && now >= buzzerOffAt) {
    noTone(BUZZER_PIN);
    buzzerActive = false;
    Serial.println("Buzzer stopped.");
  }

  if (thresholdCrossed && !buzzerActive && now >= nextAllowedEventAt) {
    startAlert(now, accMag, gyroMag);
  }

  delay(10); // approx. 100 Hz
}
