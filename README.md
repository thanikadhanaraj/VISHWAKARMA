# VISHWAKARMA
## CARESAFE — AI and Edge-Computing Based Wearable Elderly Fall Detection System

**An IoT-enabled wearable prototype for elderly safety monitoring and caregiver alerts.**

### 📌 Overview

CARESAFE is a wearable safety monitoring system designed to support elderly people living independently. It combines motion sensing, GPS location tracking, audible alerts, and physiological monitoring in a connected IoT architecture.

The waist-worn unit uses an ESP32 and an MPU6050 motion sensor to identify potential fall-related motion events. A GPS module provides location coordinates, while a buzzer generates a local warning. A wrist-worn optical sensor prototype measures heart rate and SpO₂, with readings intended for remote monitoring through the Blynk IoT dashboard.

### ✨ Key Features

- **Potential Fall Detection:** Uses accelerometer and gyroscope measurements to detect candidate motion events.
- **GPS Location Tracking:** Retrieves latitude and longitude when a valid GPS fix is available.
- **Local Audio Alert:** Activates a buzzer when the motion-event threshold is crossed.
- **Heart Rate Monitoring:** Uses a MAX30102 optical sensor to estimate heart rate.
- **SpO₂ Monitoring:** Estimates peripheral oxygen saturation from red and infrared optical signals.
- **IoT Dashboard:** Uses Blynk to display sensor data and support remote monitoring.
- **Modular Architecture:** Separates waist-based motion monitoring from wrist-based physiological sensing.

### 🏗️ System Architecture

```text
             CARESAFE WAIST UNIT
       ┌──────────────────────────┐
       │ ESP32-WROOM-32           │
       │                          │
       │ MPU6050 Motion Sensor    │
       │ GPS Module               │
       │ Buzzer                   │
       └────────────┬─────────────┘
                    │ Wi-Fi
                    ▼
             ┌──────────────┐
             │ Blynk IoT    │
             │ Dashboard    │
             └──────────────┘

             CARESAFE WRIST UNIT
       ┌──────────────────────────┐
       │ ESP32-WROOM-32           │
       │ MAX30102 Optical Sensor  │
       │ Heart Rate / SpO₂        │
       └────────────┬─────────────┘
                    │ Wi-Fi
                    ▼
             ┌──────────────┐
             │ Blynk IoT    │
             │ Dashboard    │
             └──────────────┘
```

*The waist and wrist units are separate ESP32 devices. Their integration into a unified monitoring interface is a future development step unless implemented in the current build.*

### 🔧 Hardware Requirements

| Component | Purpose |
|---|---|
| ESP32-WROOM-32 | Main controller for each unit |
| MPU6050 | Acceleration and angular-velocity measurements |
| GPS module (GY-NEO6MV2) | Latitude and longitude |
| MAX30102 / HW-058 | Optical heart-rate and SpO₂ estimation |
| Active/passive buzzer | Local audible alert |
| Battery and suitable power circuitry | Portable operation |
| Jumper wires and wearable attachment | Prototyping and assembly |

### 💻 Software and Technologies

- **Programming:** Embedded C/C++ for ESP32
- **Development Environment:** Arduino IDE
- **IoT Platform:** Blynk
- **Communication:** Wi-Fi, I²C, UART
- **Sensor Libraries:** Adafruit MPU6050, TinyGPSPlus, SparkFun MAX3010x
- **Processing:** Motion-threshold logic and optical-sensor measurement algorithms

### ⚙️ How It Works

1. The MPU6050 continuously measures acceleration and angular velocity.
2. The ESP32 evaluates the measurements against configured motion thresholds.
3. When a threshold is crossed, the system generates a candidate motion alert and activates the buzzer.
4. The GPS module supplies location coordinates when satellite reception provides a valid fix.
5. The wrist unit processes red and infrared optical samples to estimate heart rate and SpO₂.
6. The ESP32 units send their respective data to Blynk for remote visualization.

### 🚀 Setup Instructions

#### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

#### 2. Install the Required Tools

- Install Arduino IDE.
- Install the ESP32 board package.
- Install the required sensor libraries through Arduino Library Manager.

#### 3. Configure the Credentials

Before uploading the sketches, configure your own Wi-Fi credentials, Blynk template information, and device-specific authentication tokens.

**Never commit Wi-Fi passwords, Blynk tokens, or other secrets to a public repository.** Use a separate private configuration file or an example configuration containing placeholders.

#### 4. Upload the Firmware

- Connect the waist ESP32 and upload the waist-unit sketch.
- Connect the wrist ESP32 and upload the wrist-unit sketch.
- Select the correct ESP32 board and serial port in Arduino IDE.

#### 5. Configure Blynk

Create the required template, device, datastreams, and dashboard widgets. Ensure each firmware sketch uses the correct device token and virtual pins.

#### 6. Test the System

- Verify MPU6050 sensor readings.
- Confirm GPS coordinates when a valid fix is available.
- Test the buzzer using safe, controlled movements.
- Evaluate optical-sensor readings under stationary conditions.
- Confirm that the dashboard receives the expected values.

### 📊 Current Development Status

- Waist-unit motion sensing: implemented and tested.
- GPS coordinate acquisition: tested with a valid GPS fix.
- Buzzer alert: tested for threshold-crossing motion events.
- Blynk waist dashboard: operational.
- Wrist optical sensing: implemented, but heart-rate and SpO₂ readings require further validation.
- Unified waist–wrist monitoring: ongoing integration.
- Caregiver low-heart-rate notification: planned for implementation and testing.

### 🔮 Future Enhancements

- Improve motion classification using a trained machine-learning model.
- Reduce false alarms using multi-stage event validation.
- Improve wrist-sensor signal quality and motion-artifact rejection.
- Implement validated low-heart-rate notification logic.
- Integrate waist and wrist measurements into a unified dashboard.
- Add battery monitoring, low-power operation, and sensor-failure detection.
- Evaluate performance across more participants and real-world conditions.

### ⚠️ Limitations and Safety

CARESAFE is an experimental prototype and is not a certified medical device. A threshold-crossing motion event is not proof of a fall, and optical heart-rate and SpO₂ estimates may be inaccurate because of movement, contact quality, and other factors.

The system must not replace professional medical assessment or a validated emergency-monitoring system. Sensor accuracy, false-alarm rates, notification reliability, and overall safety require further testing.

### 👥 Project Team

- **Thanika D** — Electronics and Instrumentation Engineering
- **Shreya Srinika K S** — Electronics and Instrumentation Engineering
- **Livickshana A** — Electronics and Communication Engineering

**Project Guide:** Nishanthini S, Assistant Professor, Department of Artificial Intelligence and Machine Learning.

### 📄 License

Choose an appropriate open-source license before distributing this project. For example, the MIT License permits reuse with attribution; add a `LICENSE` file if you select it.

---

*CARESAFE — Building connected wearable technology to support safer and more independent living for older adults.*
