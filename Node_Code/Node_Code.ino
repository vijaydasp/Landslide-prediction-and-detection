#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <Wire.h>
#include <MPU6050.h>

#define DHTPIN 19
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

MPU6050 mpu;

const char* ssid     = "wait";
const char* password = "123456789";
const char* serverName = "http://192.168.205.95:5000/test";

unsigned long lastTime = 0;
unsigned long timerDelay = 1000;

int rainSensorPin = 32;
int moistureSensorPin = 35;
const int trigg = 18;
const int echo = 5;
int distance = 0;
long duration = 0;

void setup_wifi()
{
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("CONNECTING.....");
  }
  Serial.println("CONNECTED");
}

void send_data(String A)
{
  if ((millis() - lastTime) > timerDelay)
  {
    if (WiFi.status() == WL_CONNECTED)
    {
      WiFiClient client;
      HTTPClient http;
      http.begin(client, serverName);
      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String data = A;
      int httpcode = http.POST(data);
      if (httpcode > 0)
      {
        String res = http.getString();
        Serial.println(httpcode);
        Serial.println(res);
      }
      else
      {
        Serial.println("Error in sending data");
      }
      http.end();
    }
    else
    {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

void setup()
{
  Serial.begin(9600);
  setup_wifi();
  dht.begin();
  Wire.begin();
  mpu.initialize();

  pinMode(rainSensorPin, INPUT);
  pinMode(moistureSensorPin, INPUT);
  pinMode(trigg, OUTPUT);
  pinMode(echo, INPUT);

  // Verify connection to MPU6050
  if (!mpu.testConnection())
  {
    Serial.println("MPU6050 connection failed");
  }
  else
  {
    Serial.println("MPU6050 connected successfully");
  }
}

int water_level()
{
  digitalWrite(trigg, LOW);
  delayMicroseconds(2);
  digitalWrite(trigg, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigg, LOW);
  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}

void loop()
{
  int16_t ax, ay, az;
  int16_t gx, gy, gz;
  mpu.getAcceleration(&ax, &ay, &az);
  mpu.getRotation(&gx, &gy, &gz);

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t))
  {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  float rainValue = analogRead(rainSensorPin);
  float moistureValue = analogRead(moistureSensorPin);
  long mappedRainValue = map(rainValue, 4095, 0, 0, 50000);
  float mappedMoistureValue = map(moistureValue, 4095, 0, 0, 10000) / 100.0;
  int accelerationX = ax / 10;
  int dist = water_level();

  Serial.print("Humidity: ");
  Serial.println(h, 4);
  Serial.print("Temperature: ");
  Serial.println(t, 4);
  Serial.print("Rain Sensor Value: ");
  Serial.println(mappedRainValue * 2);
  Serial.print("Moisture Sensor Value: ");
  Serial.println(mappedMoistureValue * 2, 2);
  Serial.print("Acceleration X: ");
  Serial.println(accelerationX);
  Serial.print("Water Level (distance): ");
  Serial.println(dist);

  send_data(String(h) + "," + String(t) + "," + String(mappedRainValue * 2) + "," +
            String(mappedMoistureValue * 2) + "," + String(dist) + "," + String(accelerationX));

  delay(1000);
}
