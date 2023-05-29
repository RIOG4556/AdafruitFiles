# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import random
import board
import adafruit_dotstar as dotstar

import gc, os
import adafruit_dotstar
import analogio
import feathers2

# On-board DotStar for boards including Gemma, Trinket, and ItsyBitsy
dots1 = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 10, brightness=0.2, auto_write=True)

feathers2.led_set(True)
# Using a DotStar Digital LED Strip with 30 LEDs connected to hardware SPI
# dots = dotstar.DotStar(board.SCK, board.MOSI, 30, brightness=0.2)

# Using a DotStar Digital LED Strip with 30 LEDs connected to digital pins
dots = dotstar.DotStar(board.D9, board.D6, 10, brightness=0.2)


# HELPERS
# a random color 0 -> 192
def random_color():
    return 255


# MAIN LOOP
n_dots = len(dots)
while True:
    # Fill each dot with a random color
    for dot in range(n_dots):
        dots[dot] = (random_color(), random_color(), random_color())
        dots1[dot] = (random_color(), random_color(), random_color())
    feathers2.led_blink()
    time.sleep(0.25)