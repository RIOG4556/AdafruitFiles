# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_scd4x
import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix

# --| User Config |----
CO2_CUTOFFS = (1000, 2000, 2500)
UPDATE_RATE = 0.5


# Set Up CO2 Sensor
i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

#set up display
# the display
matrix = Matrix(width=64, height=32, bit_depth=6)
display = matrix.display
display.rotation = 90  # matrixportal up
# display.rotation = 270 # matrixportal down

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

# current condition smiley face
smileys_bmp, smileys_pal = adafruit_imageload.load("/bmps/smileys.bmp")
smiley = displayio.TileGrid(
    smileys_bmp,
    pixel_shader=smileys_pal,
    x=0,
    y=6,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
)

# current condition label
tags_bmp, tags_pal = adafruit_imageload.load("/bmps/tags.bmp")
label = displayio.TileGrid(
    tags_bmp,
    pixel_shader=tags_pal,
    x=0,
    y=37,
    width=1,
    height=1,
    tile_width=32,
    tile_height=16,
)

# current CO2 value
digits_bmp, digits_pal = adafruit_imageload.load("/bmps/digits.bmp")
co2_value = displayio.TileGrid(
    digits_bmp,
    pixel_shader=digits_pal,
    x=0,
    y=54,
    width=4,
    height=1,
    tile_width=8,
    tile_height=10,
)
# current Temp&Humidity value
digits_bmp, digits_pal = adafruit_imageload.load("/bmps/digits.bmp")
temp_value = displayio.TileGrid(
    digits_bmp,
    pixel_shader=digits_pal,
    x=0,
    y=0,
    width=4,
    height=1,
    tile_width=8,
    tile_height=10,
)

sprite_sheet, palette = adafruit_imageload.load("/bmps/cp_sprite_sheet.bmp")
# Create a sprite (tilegrid)
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            x=0,
                            y=0,
                            width = 1,
                            height = 1,
                            tile_width = 16,
                            tile_height = 16)


# put em all together
splash = displayio.Group()
splash.append(smiley)
splash.append(label)
splash.append(co2_value)
splash.append(temp_value)
splash.append(sprite)

# and show em
display.show(splash)


def update_display(value):

    value = abs(round(value))

    # smiley and label
    if value < CO2_CUTOFFS[0]:
        smiley[0] = label[0] = 0
    elif value < CO2_CUTOFFS[1]:
        smiley[0] = label[0] = 1
    elif value < CO2_CUTOFFS[2]:
        smiley[0] = label[0] = 2
    else:
        smiley[0] = label[0] = 3

    # CO2 value
    # clear it
    for i in range(4):
        co2_value[i] = 10
    # update it
    i = 3
    while value:
        co2_value[i] = value % 10
        value = int(value / 10)
        i -= 1



def Update_TempHumid(value2):
    value2 = abs(round(value2))
    # CO2 value
    # clear it
    for i in range(4):
        temp_value[i] = 10
    # update it
    i = 3
    while value2:
        temp_value[i] = value2 % 10
        value2 = int(value2 / 10)
        i -= 1

def display_sprite():
    sprite[0] = 5
    sprite.x = 8
    sprite.y = 0
    time.sleep(1)
    sprite.x = 2
    sprite.y = 0









while True:

    # protect against NaNs and Nones
    if scd4x.data_ready:
        update_display(scd4x.CO2)
        time.sleep(1)
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
        display_sprite()
        time.sleep(1)
        Update_TempHumid(scd4x.temperature)
        time.sleep(3)
        Update_TempHumid(scd4x.relative_humidity)
        time.sleep(1)


    else:
        pass
    time.sleep(UPDATE_RATE)
