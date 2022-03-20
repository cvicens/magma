import time
import json
import terminalio
import digitalio
import random
import board
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_magtag.magtag import Graphics
from adafruit_display_shapes.rect import Rect


# DisplayIO setup
font_statement = bitmap_font.load_font("/fonts/Arial-12.pcf")
font_title = bitmap_font.load_font("/fonts/Arial-Bold-12.pcf")

# Import cards
deck = {}
with open("deck.json") as fp:
    deck = json.load(fp)

# Shuffle the deck
cards = sorted(deck["items"], key=lambda _: random.random())

if len(cards) > 0:
    graphics = Graphics(auto_refresh=False)
    display = graphics.display
    print(display)

    background = Rect(0, 0, 296, 128, fill=0xFFFFFF)
    graphics.splash.append(background)

    label_title = Label(
        font_title,
        x=0,
        y=10,
        line_spacing=0.75,
        color=0x000000,
        text=deck["title"],
    )
    graphics.splash.append(label_title)

    label_statement = Label(
        font_statement, x=0, y=25, line_spacing=0.75, color=0x000000, padding_left=15
    )
    graphics.splash.append(label_statement)

    label_statement.text = (cards[0]["statement"])
    
    graphics.qrcode(cards[0]["solution"], qr_size=2, x=237, y=67)
    #graphics.qrcode("https://google.es", qr_size=2, x=240, y=70)
    board.DISPLAY.show(graphics.splash)
    display.refresh()


