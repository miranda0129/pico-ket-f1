import network
import time
from secrets import SSID, PASSWORD

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        print(wlan.isconnected())
        print(wlan.ifconfig())

        while not wlan.isconnected():
            time.sleep(1)

    return wlan