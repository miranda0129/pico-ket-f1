
from secrets import SSID, PASSWORD
from wifi import connect

import network
import requests
import time
import ntptime

UTC_OFFSET = -4 * 60 * 60  # UTC-4

def format_time(timestamp, utc_offset=-4*60*60):
    t = time.localtime(timestamp + utc_offset)

    return "{:04}-{:02}-{:02} {:02}:{:02}".format(
        t[0], t[1], t[2], t[3], t[4]
    )

def parse_jolpica_time(date, time_str):
    """
    Convert Jolpica date/time into Unix timestamp.
    Example:
    date = '2026-07-18'
    time_str = '14:00:00Z'
    """

    time_str = time_str.replace("Z", "")

    year, month, day = [int(x) for x in date.split("-")]
    hour, minute, second = [int(x) for x in time_str.split(":")]

    return time.mktime(
        (year, month, day, hour, minute, second, 0, 0)
    )

def print_next_session():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~                                                ~')
    print('~             Next upcoming session              ~')
    print('~                                                ~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

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
          print('Name: ' + str(next_session["name"]))
          print('Time: ' + str(format_time(next_session["time"])))
        else:
          print("No upcoming sessions")

def print_drivers_standings():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~                                                ~')
    print('~                 DWC Standings                  ~')
    print('~                                                ~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    url = "https://api.jolpi.ca/ergast/f1/current/driverStandings.json"
    response = requests.get(url)
    data = response.json()

    driverStandings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    for driver in driverStandings:
        print(driver["Driver"]["givenName"], driver["Driver"]["familyName"] + ' : ' + driver["points"])

def print_constructors_standings():
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('~                                                ~')
    print('~             Constructors Standings             ~')
    print('~                                                ~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    url = "https://api.jolpi.ca/ergast/f1/current/constructorStandings.json"
    response = requests.get(url)
    data = response.json()

    constructorStandings = data["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

    for constructor in constructorStandings: 
        print(constructor["Constructor"]["constructorId"] + ' : ' + constructor["points"])

wifi = connect()
ntptime.settime()

print_drivers_standings()
print_constructors_standings()
print_next_session()

