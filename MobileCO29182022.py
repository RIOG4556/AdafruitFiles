# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid white
background, a smaller black rectangle, and some white text.
"""

import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import time
import board
import adafruit_scd4x

displayio.release_displays()

oled_reset = board.D9

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d, reset=oled_reset)

#newcode
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])
scd4x.start_periodic_measurement()
print("Waiting for first measurement....")




WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
#text = "CO2:"
text_area = label.Label(
    terminalio.FONT, text="CO2 Monitor", color=0xFFFFFF, x=25, y=HEIGHT // 2 - 1
)

splash.append(text_area)

while True:

    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
        text_area.text = "{:4.1f}""ppm".format(scd4x.CO2)
        time.sleep(3)
        text_area.text = "{:4.1f}""C".format(scd4x.temperature)
        time.sleep(2)
        text_area.text = "{:4.1f}""%".format(scd4x.relative_humidity)





    time.sleep(1)

    pass

