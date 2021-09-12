#include <Arduino.h>
#include <WiFi.h>
#include <ESP32Ping.h>
#include <HTTPClient.h>

#include "pb_common.h"
#include "pb.h"
#include "pb_encode.h"

#include "config.h"

#define BAUD_RATE 115200

void setup()
{
  Serial.begin(BAUD_RATE);
  delay(1000);
  WiFi.begin(SSID);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi!");
  Serial.printf("Mac address: ");
  Serial.println(WiFi.macAddress());

  bool success = Ping.ping("www.google.com", 3);

  if (!success)
  {
    Serial.println("Ping failed");
    exit(-1);
  }

  Serial.println("Ping succesful.");
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    exit(-1);
  }

  HTTPClient http;

  http.addHeader("x-api-key", MTA_API_KEY);
  int httpCode = http.GET();
  Serial.println(httpCode);
  if (httpCode > 0)
  {
    Serial.println(http.headers());
  }
  else
  {
    Serial.println("Error on HTTP request");
  }
  delay(2000);
}
