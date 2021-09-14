using namespace std;

#define API_URL "https://api.us-east-1.amazonaws.com/transit-data"
const string API_PASSWORD = "password";

const string ROOT_CA = \
"-----BEGIN CERTIFICATE-----\n" \
"...\n" \
"-----END CERTIFICATE-----\n";

#define NTPServer "pool.ntp.org"
// -5 for eastern standard time
#define Timezone -5

// #define SSID "The House"
#define SSID "SSID"
#define PASSWORD (const char *)__null

#define LED_PIN 15
