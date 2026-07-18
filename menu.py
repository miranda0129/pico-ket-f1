from machine import Pin, SPI
import time
import ntptime
import requests
from OLED_1in3 import OLED_1inch3
from wifi import connect
from displayControl import strip_accents
from wdc import draw_wdc_standings

oled = OLED_1inch3()

next = Pin(15, Pin.IN, Pin.PULL_UP)
previous = Pin(17, Pin.IN, Pin.PULL_UP)

index = 0
next_pressed = False
prev_pressed = False

offset = 0
scrolling = False
last_scroll = time.time()
scroll_delay = 1

def draw_menu():
    global index

    menu_items = ["WDCC", "Constructors"]
    oled.fill(0)

    for item, menu_item in enumerate(menu_items):
        print(item, menu_item, index)
        if item == index:
            menu_items[index] += " ! "

    for i, menu_item in enumerate(menu_items):
        oled.text(menu_item, 0, i * 16, 1)

spi = SPI(
    1,
    baudrate=10000000,
    polarity=0,
    phase=0,
    sck=Pin(10),
    mosi=Pin(11)
)