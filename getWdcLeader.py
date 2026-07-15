
import network
import requests
from wifi import connect
import ntptime

wifi = connect()
ntptime.settime()

url = "https://api.jolpi.ca/ergast/f1/current/driverStandings.json"

response = requests.get(url)
data = response.json()

leader = data["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"][0]

print(leader["Driver"]["givenName"], leader["Driver"]["familyName"])
print(leader["points"])