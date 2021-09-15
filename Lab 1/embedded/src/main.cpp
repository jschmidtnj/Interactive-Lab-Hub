#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
#include <iostream>
#include <iomanip>
#include <sstream>

#include "ESP32Ping.h"
#include "FastLED.h"
#include "ArduinoJson.h"

#include "config.h"

using namespace std;

CRGB leds[NUM_LEDS];

int lastUpdate;

const int updateDelta = UPDATE_MINUTES * 60 * 1000;

tm get_time()
{
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo))
  {
    Serial.println("Failed to obtain time");
    return;
  }
  return timeinfo;
}

string time_to_string(tm tm)
{
  stringstream ss;
  ss << put_time(&tm, "%c");
  return ss.str();
}

void print_time(tm tm)
{
  // Serial.println(time_to_string(tm).c_str());
  Serial.println(&tm, "%A, %B %d %Y %H:%M:%S");
}

void print_local_time()
{
  tm tm = get_time();
  print_time(tm);
}

tm parse_time(const char *timeStr)
{
  struct tm tm;
  istringstream iss(timeStr);
  iss >> get_time(&tm, "%Y-%m-%dT%H:%M:%SZ");
  if (iss.fail())
  {
    Serial.println("timestamp parse failed");
    return;
  }
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
  Serial.print("current time: ");
  print_local_time();
}

void setup()
{
  Serial.begin(BAUD_RATE);
  FastLED.addLeds<CHIPSET, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(COLOR_CORRECTION);
  FastLED.setBrightness(BRIGHTNESS);

  init_wifi();
}

vector<tm> convert_to_times(vector<const char *> &data)
{
  vector<tm>times(data.size());
  for (const char * &curr_time: data) {
    times.push_back(parse_time(curr_time));
  }
  return times;
}

struct closest_time_res {
  tm closest_time;
  int time_remaining;
};

closest_time_res* get_closest_time(vector<tm> times, int transit_time_minutes)
{
  // sort times
  sort(times.begin(), times.end());
  time_t now = mktime(&get_time());
  for (tm &curr_time: times) {
    double seconds = difftime(mktime(&curr_time), now) - 60 * transit_time_minutes;
    if (seconds >= 0) {
      return &closest_time_res({
        curr_time,
        (int)seconds
      });
    }
  }
  return NULL;
}

// time_remaining is in seconds
CRGB get_color(int time_remaining)
{
  // colors
  CRGB good_color(0x2cd459);
  CRGB warning_color(0xfff82e);
  CRGB danger_color(0xf7501e);

  // all in minutes
  const int good = 10; // have lots of time
  const int warning = 5; // warning
  const int danger = 2; // little time left

  if (time_remaining >= 60 * good) {
    return good_color;
  }
  if (time_remaining >= 60 * warning) {
    return blend(good_color, warning_color, (time_remaining / 60.0 - warning) / (good - warning));
  }
  if (time_remaining >= 60 * danger) {
    return blend(warning_color, danger_color, (time_remaining / 60.0 - danger) / (warning - danger));
  }
  return danger_color;
}

struct data_type_res {
  vector<const char *> subway;
  vector<const char *> ferry;
  vector<const char *> tram;
};

data_type_res* get_data()
{
  HTTPClient http;

  http.begin(API_URL, ROOT_CA.c_str());
  http.addHeader("Authorization", ("Bearer " + API_PASSWORD).c_str());
  int httpCode = http.GET();
  if (httpCode != HTTP_CODE_OK)
  {
    Serial.println("Error on HTTP request");
    http.end();
    return NULL;
  }

  DynamicJsonDocument doc(1024);
  DeserializationError JSONError = deserializeJson(doc, http.getStream());
  http.end();
  if (JSONError)
  {
    Serial.print("JSON deserialization failed: ");
    Serial.println(JSONError.f_str());
    return NULL;
  }
  data_type_res res({
    doc["subway"],
    doc["ferry"],
    doc["tram"],
  });
  return &res;
}

void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    exit(-1);
  }

  if (millis() - lastUpdate > updateDelta)
  {
    lastUpdate = millis();
    auto data = get_data();
    if (data == NULL) {
      return;
    }
    closest_time_res * subway_closest_time = get_closest_time(convert_to_times(data->subway), MINUTES_TO_SUBWAY);
    int time_to_subway = subway_closest_time != NULL ? subway_closest_time->time_remaining : INT_MAX;
    leds[SUBWAY_LED] = get_color(time_to_subway);

    closest_time_res * ferry_closest_time = get_closest_time(convert_to_times(data->ferry), MINUTES_TO_FERRY);
    int time_to_ferry = ferry_closest_time != NULL ? ferry_closest_time->time_remaining : INT_MAX;
    leds[FERRY_LED] = get_color(time_to_ferry);

    closest_time_res * tram_closest_time = get_closest_time(convert_to_times(data->tram), MINUTES_TO_TRAM);
    int time_to_tram = tram_closest_time != NULL ? tram_closest_time->time_remaining : INT_MAX;
    leds[TRAM_LED] = get_color(time_to_tram);
  }

  FastLED.show();
  FastLED.delay(100);
}
