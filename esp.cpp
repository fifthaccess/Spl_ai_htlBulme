#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char SSID = "DietPi-HotSpot";
const charPWD = "dietpihotspot";
const char* mqttServer = "172.16.119.10"; 
const int mqttPort = 1883; 
const int ledPin = 2;
const int signalPin = 4;

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void callback(char* topic, byte* payload, unsigned int length) {
  // Nachricht empfangen
  Serial.print("Nachricht empfangen: ");
  /*for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  */
  Serial.println();

  //LED einschalten
  if ((char)payload[0] == '1'){
    Serial.println("1 recieved");
    digitalWrite(ledPin, HIGH);
  }
  // LED auschalten
  else if((char)payload[0] == '0'){
    Serial.println("0 recieved");
    digitalWrite(ledPin, LOW);
  } 
}

void connectToWiFi() {
  Serial.print("Verbinde mit WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi verbunden");
}

void connectToMQTT() {
  Serial.print("Verbinde mit MQTT-Broker...");
  while (!mqttClient.connected()) {
    if (mqttClient.connect("ESP32Client")) {
      Serial.println("verbunden");
      mqttClient.subscribe("testTopic");
    } else {
      Serial.print("Fehlgeschlagen, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Versuche es erneut in 5 Sekunden...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(signalPin, INPUT);

  connectToWiFi();
  mqttClient.setServer(mqttServer, mqttPort);
  mqttClient.setCallback(callback);
}

void loop() {
  if (!mqttClient.connected()) {
    connectToMQTT();
  }
  mqttClient.loop();
}