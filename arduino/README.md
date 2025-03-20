# Garduino - Arduino Code

This repository contains the Arduino/ESP32 code for the Garden Project. The code reads data from a Captive Soil Moisture Sensor v1.2 and a DS18B20 Temperature Sensor, then sends the sensor data via WiFi to a master node for further processing and visualization.

## Table of Contents
- [Overview](#overview)
- [Hardware Components](#hardware-components)
- [Wiring Diagram](#wiring-diagram)
- [Software Requirements](#software-requirements)
- [Installation and Setup](#installation-and-setup)
- [Code Overview](#code-overview)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

The ESP32 reads:
- **Soil Moisture:** Using an analog sensor.
- **Temperature:** Using a DS18B20 digital sensor over OneWire.

It then packages the readings into a JSON object and sends an HTTP POST to the master node at a predefined URL.

## Hardware Components

- **ESP32 Microcontroller**
- **Captive Soil Moisture Sensor v1.2**
- **DS18B20 Temperature Sensor**
- **4.7KΩ Resistor** (for DS18B20 pull-up)
- Breadboard and jumper wires

## Wiring Diagram

### DS18B20 Temperature Sensor
- **VCC:** Connect to 3.3V on the ESP32.
- **GND:** Connect to GND on the ESP32.
- **Data:**  
  - Connect to **GPIO4** (or another digital GPIO pin you choose).
  - **Pull-Up Resistor:** Place a 4.7KΩ resistor between the data line and the 3.3V pin.

### Soil Moisture Sensor
- **VCC:** Connect to 3.3V (or 5V, based on sensor specs—ensure safe voltage for ESP32 ADC).
- **GND:** Connect to GND.
- **Analog Output:** Connect to **GPIO34** (or another ADC-capable pin).

## Software Requirements

- **Arduino IDE** (version 1.8.13 or later recommended)
- **ESP32 Board Package**  
  [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- **Arduino Libraries:**  
  - [OneWire](https://github.com/PaulStoffregen/OneWire) (by Paul Stoffregen)  
  - [DallasTemperature](https://github.com/milesburton/Arduino-Temperature-Control-Library) (by Miles Burton)

## Installation and Setup

1. **Install the ESP32 Board Package:**
   - In the Arduino IDE, navigate to **File > Preferences**.
   - In "Additional Board Manager URLs", add:
     ```
     https://dl.espressif.com/dl/package_esp32_index.json
     ```
   - Then go to **Tools > Board > Boards Manager**, search for "esp32", and install the package.

2. **Install Required Libraries:**
   - Go to **Sketch > Include Library > Manage Libraries**.
   - Search for and install the "OneWire" library.
   - Search for and install the "DallasTemperature" library.

3. **Open the Sketch:**
   - Open the provided `soil_temp_sensor.ino` file in the Arduino IDE.

4. **Configure the Code:**
   - Verify the pin assignments match your wiring (GPIO4 for DS18B20 and GPIO34 for the soil moisture sensor).
   - Update the WiFi credentials (SSID and password) and the server URL in the code:
     ```cpp
     const char* ssid = "Your_SSID";
     const char* password = "Your_Password";
     const char* serverURL = "http://<master-node-ip>:5000/soil-data";
     ```

5. **Upload the Code:**
   - Connect your ESP32 via USB.
   - Select the correct board (e.g., ESP32 Dev Module) and port in the Arduino IDE.
   - Click the **Upload** button.

## Code Overview

- **Setup Section:**  
  - Initializes WiFi and waits for connection.
  - Starts the DS18B20 sensor.
- **Loop Section:**  
  - Reads the soil moisture value using `analogRead` on GPIO34.
  - Requests and reads the temperature from the DS18B20 sensor.
  - Constructs a JSON payload with the format:
    ```json
    {"soil_moisture": <value>, "temperature": <value>}
    ```
  - Sends the JSON payload to the master node using an HTTP POST.
  - Waits 60 seconds before the next reading.

## Troubleshooting

- **WiFi Issues:**  
  Ensure your ESP32 is within range and the SSID/password are correct.
- **Compilation Errors:**  
  Make sure the ESP32 board package and required libraries (OneWire, DallasTemperature) are installed.
- **Upload Problems:**  
  Verify the correct COM port and board are selected. Refer to troubleshooting guides if you have boot mode issues.
- **Sensor Readings:**  
  If values appear incorrect, double-check your wiring connections and resistor placement for the DS18B20.
- **Server Communication:**  
  Verify the master node URL and that the server is accessible from the ESP32.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the ESP32 community for providing extensive resources.
- Appreciation to the developers of the OneWire and DallasTemperature libraries.
- Inspired by various DIY garden and IoT projects.

