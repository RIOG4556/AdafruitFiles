# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_scd4x
import displayio
import adafruit_imageload
from adafruit_matrixportal.matrix import Matrix
import adafruit_bh1750

# --| User Config |----
CO2_CUTOFFS = (1000, 2000, 2500)
UPDATE_RATE = 0.5




# Create a two color palette
palette2 = displayio.Palette(2)
palette2[0] = 0xFF0000
palette2[1] = 0x0000FF


palette3 = displayio.Palette(2)
palette3[0]= 0x000000
palette3[1] = 0xFF0000




# Set Up CO2 Sensor
i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
sensor = adafruit_bh1750.BH1750(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

#set up display
# the display
matrix = Matrix(width=64, height=32, bit_depth=6)
display = matrix.display
display.rotation = 90  # matrixportal up
# display.rotation = 270 # matrixportal down
# Create a bitmap with two colors
bitmap2 = displayio.Bitmap(2, 2, 2)
bitmap3 = displayio.Bitmap(30,60,2)

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



# Create a TileGrid using the Bitmap and Palette
tile_grid2 = displayio.TileGrid(bitmap2, pixel_shader=palette2)
tile_grid3 = displayio.TileGrid(bitmap3,pixel_shader=palette3)
# put em all together
splash = displayio.Group()
splash2 = displayio.Group()
splash.append(smiley)
splash.append(label)
splash.append(co2_value)
splash.append(temp_value)
splash.append(tile_grid2)
splash2.append(tile_grid3)

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



def button2():

    bitmap2[0,0] = 0
    bitmap2[1, 0] = 0
    bitmap2[1,1] = 0
    bitmap2[0, 1] = 0
    time.sleep(1)
    bitmap2[0,0] = 1
    bitmap2[1, 0] = 1
    bitmap2[1,1] = 1
    bitmap2[0, 1] = 1

def off():
    display.show(splash2)
















while True:
    if sensor.lux < 10:
        print ("off")
        off()
        time.sleep(1)
        pass


    #show all sections including signal bitmap(button) in corner
    elif scd4x.data_ready:
        display.show(splash)
        print("%.2f Lux" % sensor.lux)
        time.sleep(1)
        update_display(scd4x.CO2)
        time.sleep(1)
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
        button2()
        time.sleep(3)
        Update_TempHumid(scd4x.temperature)
        time.sleep(3)
        Update_TempHumid(scd4x.relative_humidity)
        time.sleep(1)


    time.sleep(UPDATE_RATE)