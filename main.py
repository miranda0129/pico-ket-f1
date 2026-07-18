from machine import Pin, SPI
import time
import ntptime
import requests
from OLED_1in3 import OLED_1inch3
from wifi import connect
from displayControl import strip_accents
from wdc import draw_wdc_standings
from menu import draw_menu

oled = OLED_1inch3()

# -------------------------
# Global variables
# -------------------------
possibleStates = {
    "next_session": 0,
    "wdc": 1,
    "constructors": 2
}
index = 0

currentState = possibleStates.get("next_session")
next_pressed = False
prev_pressed = False

offset = 0
scrolling = False
last_scroll = time.time()
scroll_delay = 1


def next_driver(pin):
    global next_pressed
    global currentState

    next_pressed = True

def prev_driver(pin):
    global prev_pressed
    prev_pressed = True

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

def parse_jolpica_time(date, time_str):
    time_str = time_str.replace("Z", "")

    year, month, day = [int(x) for x in date.split("-")]
    hour, minute, second = [int(x) for x in time_str.split(":")]

    return time.mktime(
        (year, month, day, hour, minute, second, 0, 0)
    )

def format_time(timestamp, utc_offset=-7*60*60):
    t = time.localtime(timestamp + utc_offset)

    return "{:04}-{:02}-{:02} {:02}:{:02}".format(
        t[0], t[1], t[2], t[3], t[4]
    )

def draw_next_sesssion():
    global last_scroll
    global offset

    url = "https://api.jolpi.ca/ergast/f1/current/next.json"

    response = requests.get(url)
    data = response.json()

    race = data["MRData"]["RaceTable"]["Races"][0]

    sessions = ["FirstPractice", "SecondPractice", "ThirdPractice", "Sprint", "Qualifying", "Race"]
    upcoming = []

    for session_name in sessions:
        if session_name in race:
            session = race[session_name]

            timestamp = parse_jolpica_time(
                session["date"],
                session["time"]
            )

            upcoming.append({
                "name": session_name,
                "time": timestamp
            })

    now = time.time()

    future_sessions = [
        s for s in upcoming
        if s["time"] > now
    ]

    if future_sessions:
        next_session = min(
            future_sessions,
            key=lambda x: x["time"]
        )

        if next_session:
            session_name = str(next_session["name"])
            session_time = str(format_time(next_session["time"]))
            print(session_name)
            print(session_time)

            oled.fill(0)

            oled.text(session_name, 0, 0, 1)

            # Determine if scrolling is needed
            scrolling = len(session_time) > 16

            if scrolling:
                if time.time() - last_scroll > scroll_delay:
                    oled.text(session_time, offset, 32, 1)

                    offset -= 1

                    if offset < -(len(session_time) * 8):
                        offset = 128
                        last_scroll = time.time()

                else:
                    oled.text(str(format_time(next_session["time"])), 0, 32, 1)

            else:
                oled.text(str(format_time(next_session["time"])), 0, 32, 1)


            oled.show()
        else:
            print("No upcoming sessions")

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

def main_loop():
    global currentState
    global next_pressed

    while True:
        if next_pressed:
            next_pressed = False

            if currentState == possibleStates["next_session"]:
                currentState = possibleStates["wdc"]

            elif currentState == possibleStates["wdc"]:
                currentState = possibleStates["next_session"]

        if currentState == possibleStates["next_session"]:
            draw_next_sesssion()

        elif currentState == possibleStates["wdc"]:
            draw_wdc_standings()

        time.sleep(0.1)


spi = SPI(
    1,
    baudrate=10000000,
    polarity=0,
    phase=0,
    sck=Pin(10),
    mosi=Pin(11)
)

wifi = connect()
ntptime.settime()

#main_loop()

#draw_next_sesssion()
draw_wdc_standings()