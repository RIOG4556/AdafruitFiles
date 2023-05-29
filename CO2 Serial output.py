# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import adafruit_scd4x
import random
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)
# Static 'Connecting' Text
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, (matrixportal.graphics.display.height // 2) - 1),
)

i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

# --- Display setup ---
matrix = Matrix(bit_depth=4)
sprite_group = displayio.Group()
matrix.display.show(sprite_group)

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

def update_data():
    matrixportal.set_text("Connecting", 1)
    
    # Choose a random color from colors
if len(colors) > 1 and last_color is not None:
    while color_index == last_color:
        color_index = random.randrange(0, len(colors))
else:
    color_index = random.randrange(0, len(colors))
last_color = color_index

while True:
    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
        # Set the quote text
        matrixportal.set_text(scd4x.CO2)
        matrixportal.set_text_color(colors[color_index])
    time.sleep(1)
