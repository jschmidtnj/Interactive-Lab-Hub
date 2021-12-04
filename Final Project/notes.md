## connection with truphone

- for using truphone, you need to work with ppp0. this works, but for some reason I can't ssh into the pi when it is enabled.
- for testing: `curl --interface ppp0 http://google.com`, `ping -I ppp0 google.com`
- to start up the interface: `sudo pon`, to stop: `sudo poff`
- connection method that didn't work: https://docs.sixfab.com/page/setting-up-a-data-connection-over-qmi-interface-using-libqmi
- instructions for working with other sims: https://docs.sixfab.com/docs/getting-started-with-cellular-hat-other-sim
- instructions for getting ppp0 connection working (works): https://docs.sixfab.com/page/setting-up-the-ppp-connection-for-sixfab-shield-hat
  - need to use `iot.truphone.com` as APN, and don't run on startup (script is broken)
- ECM mode is not available, but commands in this link mostly work: https://docs.sixfab.com/page/internet-connection-with-telit-le910c1-module-using-ecm-mode
- if I had the lte version this would be useful: https://docs.sixfab.com/page/internet-connection-with-twilio-super-sim-telit-le910x-and-sixfab-base-hat-using-ecm
- useful post: https://community.sixfab.com/t/3g-4g-lte-base-hat-telit-modem-error-on-configure-apn-for-inet-connection-with-ecm/1072/7
- truphone dashboard: https://iot.truphone.com/dashboard/

## connection with sixfab

- instructions: https://docs.sixfab.com/docs/raspberry-pi-cellular-iot-kit-getting-started
