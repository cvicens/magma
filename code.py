import time
# from adafruit_datetime import datetime
import alarm
import json
# import terminalio
# import digitalio
import random
import board
import ssl
import wifi
import socketpool
import adafruit_requests

from adafruit_display_text.label import Label
from adafruit_display_text import wrap_text_to_lines
from adafruit_bitmap_font import bitmap_font
from adafruit_magtag.magtag import Graphics
from adafruit_display_shapes.rect import Rect


# DisplayIO setup
font_statement = bitmap_font.load_font("/fonts/Arial-12.pcf")
font_title = bitmap_font.load_font("/fonts/Arial-Bold-12.pcf")

# URLs to fetch from
JSON_NEWS_URL = "https://www.adafruit.com/api/quotes.php"

# Display Time in Seconds
DISPLAY_TIME = 5

# Left COL SIZE
LEFT_COL_SIZE = 65

def title_transform(title):
    if title == None or not len(title):
        return "No text found... ask Daddy"
    return title[0:30]

def text_transform(text):
    if text == None or not len(text):
        return "No text found... ask Daddy"
    return "\n".join(wrap_text_to_lines(text[0:166] + "...", 28))

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s"%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("Fetching json from", JSON_NEWS_URL)
response = requests.get(JSON_NEWS_URL)
print("-" * 40)
print(response.json())
print("-" * 40)

# Import cards
news = []
with open("news.json") as fp:
    news = json.load(fp)

# Shuffle the news
# sortedNews = sorted(news, key=lambda x: datetime.fromisoformat(x['date']), reverse=True)
sortedNews = news

if len(sortedNews) > 0:
    for item in sortedNews:
        graphics = Graphics(auto_refresh=False)
        display = graphics.display

        time.sleep(display.time_to_refresh)
        time.sleep(DISPLAY_TIME)

        background = Rect(0, 0, 296, 128, fill=0xFFFFFF)
        graphics.set_background("/bmps/" + item['type'] + ".bmp")
        # graphics.splash.append(background)

        label_title = Label(
            font_title,
            x=LEFT_COL_SIZE,
            y=10,
            line_spacing=0.75,
            color=0x000000,
            text=title_transform(item['title']),
        )
        graphics.splash.append(label_title)

        label_statement = Label(
            font_statement, 
            x=LEFT_COL_SIZE, 
            y=25, 
            line_spacing=0.75, 
            color=0x000000, 
            padding_left=15, 
            text_wrap=47,
            text=text_transform(item['text']),
        )
        graphics.splash.append(label_statement)

        # label_statement.text = (item['text'])
        
        if 'url' in item:
            graphics.qrcode(item['url'], qr_size=2, x=0, y=67)
        board.DISPLAY.show(graphics.splash)
        display.refresh()
        

# Create a an alarm that will trigger 20 seconds from now.
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 20)
# Exit the program, and then deep sleep until the alarm wakes us.
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
# Does not return, so we never get here.
