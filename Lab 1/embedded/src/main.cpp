#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>

#include "ESP32Ping.h"
#include "FastLED.h"

#include "config.h"

using namespace std;

#define BAUD_RATE 115200
#define NUM_LEDS 3
#define COLOR_ORDER RGB
#define CHIPSET WS2812B
#define BRIGHTNESS 128

#define HTTPS_PORT 443

CRGB leds[NUM_LEDS];

void printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
}

void init_wifi()
{
  delay(1000);
  Serial.println('\n');

  // connect to the network
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to ");
  Serial.println(SSID);

  Serial.printf("Mac address: ");
  Serial.println(WiFi.macAddress());

  // wait for the Wi-Fi to connect
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print('.');
  }
  Serial.println("\nConnection established.");

  bool success = Ping.ping("www.google.com", 3);

  if (!success)
  {
    Serial.println("Ping failed");
    exit(-1);
  }

  Serial.println("Ping successful.");

  configTime(Timezone * 60 * 60, 60 * 60, NTPServer);
  printLocalTime();
}

void setup()
{
  Serial.begin(BAUD_RATE);
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalSMD5050);
  FastLED.setBrightness(BRIGHTNESS);

  init_wifi();
}

void get_data()
{
  HTTPClient http;

  http.begin(API_URL, ROOT_CA.c_str());
  http.addHeader("Authorization", ("Bearer " + API_PASSWORD).c_str());
  int httpCode = http.GET();
  Serial.println(httpCode);
  if (httpCode > 0)
  {
    Serial.println(http.headers());
    Serial.println(http.getString());
  }
  else
  {
    Serial.println("Error on HTTP request");
  }
  http.end();
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    exit(-1);
  }

  leds[0] = 0xeb1000;
  leds[1] = 0x00eb23;
  leds[2] = 0x00eb23;
  FastLED.show();
  FastLED.delay(8);
}
