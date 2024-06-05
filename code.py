import adafruit_connection_manager
import adafruit_ntp
import os
import time
import wifi
import led8seg

wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")

display = led8seg.LED_8SEG()

while True:
    try:
        wifi.radio.connect(wifi_ssid, wifi_password)
        break
    except:
        print("failed")
        continue

pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=-6)

previous_second = None  # store the previous second value

while True:
    try:
        netTime = ntp.datetime
        hour = netTime.tm_hour
        minute = netTime.tm_min
        current_second = netTime.tm_sec

        # print only if the current second is different from the previous one
        if previous_second != current_second:
            print(
                f"It is {hour}:{'0' if minute < 10 else ''}{minute}:{'0' if current_second < 10 else ''}{current_second}"
            )
            previous_second = current_second  # update for next iteration
        display.display_number(int(f"{hour}{'0' if minute < 10 else ''}{minute}"))

        time.sleep(0.002)
    except:
        continue
