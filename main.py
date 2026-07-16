from machine import Pin, SPI
import time
import ntptime
import requests
from OLED_1in3 import OLED_1inch3
from wifi import connect

def scroll_text(oled, text, y, speed=0.05):
    text_width = len(text) * 8

    # Show full text first
    oled.fill_rect(0, y, 128, 8, 0)
    oled.text(text, 0, y, 1)
    oled.show()

    # Wait before scrolling
    time.sleep(1)

    # Start scrolling
    x = 0

    while x > -text_width:
        oled.fill_rect(0, y, 128, 8, 0)
        oled.text(text, x, y, 1)
        oled.show()

        x -= 1
        time.sleep(speed)

    while x > -text_width:
        oled.fill_rect(0, y, 128, 8, 0)
        oled.text(text, x, y, 1)
        oled.show()

        x -= 1
        time.sleep(speed)


# SPI1 pins used by Waveshare Pico OLED 1.3
spi = SPI(
    1,
    baudrate=10000000,
    polarity=0,
    phase=0,
    sck=Pin(10),
    mosi=Pin(11)
)

# Create display object
oled = OLED_1inch3()

wifi = connect()
ntptime.settime()

url = "https://api.jolpi.ca/ergast/f1/current/driverStandings.json"

response = requests.get(url)
data = response.json()

leader = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]

driverName = f'{leader["Driver"]["givenName"]} {leader["Driver"]["familyName"]}'
pointsTotal = leader["points"]

print(driverName)
print(pointsTotal)

offset = 0
scrolling = len(driverName) > 16
scroll_delay = 1
start_time = time.time()

while True:
    oled.fill(0)

    # Driver name
    if scrolling:
        if time.time() - start_time > scroll_delay:
            oled.text(driverName, offset, 0, 1)
            offset -= 1

            if offset < -(len(driverName) * 8):
                offset = 128
                start_time = time.time()
        else:
            oled.text(driverName, 0, 0, 1)
    else:
        oled.text(driverName, 0, 0, 1)

    # Points always visible
    oled.text(str(pointsTotal), 0, 16, 1)

    oled.show()

    time.sleep(0.05)