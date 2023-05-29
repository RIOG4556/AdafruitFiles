import time
import board
import displayio
import terminalio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix

# Create a two color palette
palette2 = displayio.Palette(3)
palette2[0] = 0x000000  # Black background
palette2[1] = 0xFF0000  # Red
palette2[2] = 0x0000FF  # blueish

# Set up display
matrix = Matrix(width=64, height=32, bit_depth=4)
display = matrix.display
display.rotation = 90  # MatrixPortal up
# display.rotation = 270  # MatrixPortal down

# Create a Bitmap with two colors
bitmap = displayio.Bitmap(64, 32, 2)

# --- Drawing setup ---
group = displayio.Group()
# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette2)
group.append(tile_grid)
display.show(group)

# Create font and label
font = bitmap_font.load_font("Exo-Bold-42.bdf")
clock_label = Label(font)
clock_label.color = palette2[2]  # Use red color

def update_display(value):
    # Clear the display by setting all pixels to 0 (black)
    bitmap.fill(0)
    clock_label.text = str(value)  # Convert the value to a string and set it as the label text

    # Center the label on the display
    clock_label.anchor_point = (0.5, 0.5)  # Centered anchor point
    clock_label.anchored_position = (display.width // 2, display.height // 2)



    display.refresh()


    # Loop to display numbers from 1 to 8

 # Add the label to the group
group.append(clock_label)

for i in range(1, 9):
    update_display(i)
    time.sleep(1)

#while True:
    #update_display(1)
    #time.sleep(10)
