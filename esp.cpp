#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char SSID = "DietPi-HotSpot";
const charPWD = "dietpihotspot";

// MQTT client
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient); 


void callBack(char* topic, byte* payload, unsigned int length) {
  Serial.print("Callback - ");
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
}
char *mqttServer = "192.168.42.1";
int mqttPort = 1883;

void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
  // set the callback function
  mqttClient.setCallback(callBack);
}

void connectToWiFi() {
  Serial.print("Connectiog to wifi ");
 
  WiFi.begin(SSID, PWD);
  Serial.println(SSID);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.print("Connected.");

}

void reconnect() {
  Serial.println("Connecting to MQTT Broker...");
  while (!mqttClient.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);

      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Connected.");
        // subscribe to topic
        mqttClient.subscribe("testTopic");
      }

  }
}




void setup() {
  Serial.begin(9600);
  connectToWiFi();
  setupMQTT();

}

void loop() {
  if (!mqttClient.connected())
  reconnect();
  mqttClient.loop();

}