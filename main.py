from machine import Pin, SPI
import time
import ntptime
import requests
from OLED_1in3 import OLED_1inch3
from wifi import connect


# -------------------------
# Global variables
# -------------------------

index = 0
next_pressed = False
prev_pressed = False

offset = 0
scrolling = False
last_scroll = time.time()
scroll_delay = 1


# -------------------------
# Button handlers
# -------------------------

def next_driver(pin):
    global next_pressed
    next_pressed = True

def prev_driver(pin):
    global prev_pressed
    prev_pressed = True

# -------------------------
# Display functions
# -------------------------
def strip_accents(text):
    replacements = {
        "á": "a",
        "à": "a",
        "ä": "a",
        "â": "a",
        "ã": "a",
        "å": "a",

        "é": "e",
        "è": "e",
        "ë": "e",
        "ê": "e",

        "í": "i",
        "ì": "i",
        "ï": "i",
        "î": "i",

        "ó": "o",
        "ò": "o",
        "ö": "o",
        "ô": "o",
        "õ": "o",

        "ú": "u",
        "ù": "u",
        "ü": "u",
        "û": "u",

        "ñ": "n",
        "ç": "c",

        "Á": "A",
        "À": "A",
        "Ä": "A",
        "É": "E",
        "È": "E",
        "Ö": "O",
        "Ü": "U",
        "Ñ": "N",
        "Ç": "C",
    }

    for accented, plain in replacements.items():
        text = text.replace(accented, plain)

    return text


def draw_driver(driver):
    global offset
    global scrolling
    global last_scroll
    global index

    driverName = strip_accents(
        f'{driver["name"]}'
    )

    pointsTotal = driver["points"]

    oled.fill(0)

    oled.text("WDC Standings", 0, 0, 1)
    oled.text("Position: " + str(index+1), 0, 16, 1)

    # Determine if scrolling is needed
    scrolling = len(driverName) > 16

    if scrolling:
        if time.time() - last_scroll > scroll_delay:
            oled.text(driverName, offset, 32, 1)

            offset -= 1

            if offset < -(len(driverName) * 8):
                offset = 128
                last_scroll = time.time()

        else:
            oled.text(driverName, 0, 32, 1)

    else:
        oled.text(driverName, 0, 32, 1)

    oled.text("PTS: " + str(pointsTotal), 0, 48, 1)

    oled.show()


# -------------------------
# Setup OLED
# -------------------------

spi = SPI(
    1,
    baudrate=10000000,
    polarity=0,
    phase=0,
    sck=Pin(10),
    mosi=Pin(11)
)

oled = OLED_1inch3()


# -------------------------
# Buttons
# -------------------------

next = Pin(15, Pin.IN, Pin.PULL_UP)
previous = Pin(17, Pin.IN, Pin.PULL_UP)

next.irq(
    trigger=Pin.IRQ_FALLING,
    handler=next_driver
)

previous.irq(
    trigger=Pin.IRQ_FALLING,
    handler=prev_driver
)


# -------------------------
# Network setup
# -------------------------

wifi = connect()

ntptime.settime()


# -------------------------
# Get F1 standings
# -------------------------

url = "https://api.jolpi.ca/ergast/f1/current/driverStandings.json"

response = requests.get(url)
data = response.json()

driverStandings = []

for driver in data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]:
    driverStandings.append({
        "name": (
            driver["Driver"]["givenName"] + " " +
            driver["Driver"]["familyName"]
        ),
        "points": driver["points"]
    })

response.close()

del data


# -------------------------
# Main loop
# -------------------------

while True:

    if next_pressed:
        index += 1
        print('next: ' + str(index))

        # Loop back to first driver
        if index >= len(driverStandings):
            index = 0

        # Reset scrolling position
        offset = 0
        last_scroll = time.time()

        next_pressed = False

    if prev_pressed:
        index -= 1
        print('prev: ' + str(index))

        offset = 0
        last_scroll = time.time()

        prev_pressed = False


    currentDriver = driverStandings[index]

    draw_driver(currentDriver)

    time.sleep(0.05)