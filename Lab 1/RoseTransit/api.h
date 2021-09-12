
#ifndef API_H
#define API_H

#include <Arduino.h>

#include <WiFiClientSecure.h>
#include <WiFi.h>

#include "config.h"
#include <HTTPClient.h>

void init_wifi()
{
  delay(10);
  Serial.println('\n');

  // connect to the network
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to ");
  Serial.print(SSID);

  // wait for the Wi-Fi to connect
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print('.');
  }
  Serial.println("\nConnection established.");
}

String send_request()
{
  String response;
  WiFiClientSecure client; // use WiFiClientSecure class to create TLS connection

  // host
  Serial.printf("Connecting to host %s\n", HOST);
  if (!client.connect(HOST, 443))
  {
    Serial.println("Connection failed.");
    return "";
  }

  // path
  Serial.printf("Requesting url %s\n", PATH);
  client.print(String("GET ") + PATH + " HTTP/1.1\r\n" +
               "Host: " + HOST + "\r\n" +
               "User-Agent: BuildFailureDetectorESP8266\r\n" +
               "Connection: close\r\n\r\n");

  // response
  Serial.println("Request sent.");
  while (client.connected())
  {
    String line = client.readStringUntil('\n');
    if (line.charAt(0) == '#')
    {
      return line;
    }
  }
  return "";
}

// #Q5.322283333333334B6.73895
float get_time_for_train(char train, String *response)
{
  size_t s, e;
  switch (train)
  {
    case 'Q':
      s = response->indexOf('Q');
      e = response->indexOf('B');
      break;
    case 'B':
      s = response->indexOf('B');
      e = size_t(response->length());
      break;
    default:
      return 0;
  }
  String sub = response->substring(s + 1, e);
  return sub.toFloat();
}


#endif
