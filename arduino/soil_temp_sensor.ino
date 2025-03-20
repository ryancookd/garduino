#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// WiFi credentials
const char* ssid = "#########";
const char* password = "#########";

// Server URL of the master node
const char* serverURL = "http://10.0.0.33:5000/soil-data";

// Soil moisture sensor pin (analog)
int soilSensorPin = 34;

// DS18B20 settings
#define ONE_WIRE_BUS 4  // GPIO pin connected to DS18B20 data line
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  // Wait for WiFi to connect
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Start DS18B20 sensor library
  sensors.begin();
}

void loop() {
  // Read soil moisture value
  int soilMoisture = analogRead(soilSensorPin);
  Serial.println("Soil Moisture Value: " + String(soilMoisture));

  // Request temperature readings from DS18B20
  sensors.requestTemperatures();  
  float temperatureC = sensors.getTempCByIndex(0);
  Serial.println("Temperature (C): " + String(temperatureC));

  // Create JSON payload including both values
  String payload = "{\"soil_moisture\": " + String(soilMoisture) +
                   ", \"temperature\": " + String(temperatureC) + "}";
  
  // Send data to master node
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {
      Serial.println("Data sent successfully, response code: " + String(httpResponseCode));
    } else {
      Serial.println("Error sending data");
    }
    http.end();
  }
  // Delay between readings (e.g., one minute)
  delay(60000);
}