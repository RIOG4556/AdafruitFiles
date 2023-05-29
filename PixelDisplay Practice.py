
import displayio
from adafruit_matrixportal.matrix import Matrix





#set up display
# the display
matrix = Matrix(width=64, height=32, bit_depth=6)
display = matrix.display
display.rotation = 0  # matrixportal up
# display.rotation = 270 # matrixportal down

# Create a bitmap with two colors
bitmap = displayio.Bitmap(display.width, display.height, 3)


# Create a two color palette
palette = displayio.Palette(3)
palette[0] = 0x000000
palette[1] = 0x4B0082
palette[2] = 0x4B0082

# Create a TileGrid using the Bitmap and Palette
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.show(group)

# Draw a pixel
bitmap[5, 5] = 2

bitmap[20,20] = 2

bitmap[5,15] = 2

for x in range(0, 30):
    for y in range(0, 30):
        bitmap[x, y] = 1

while True:
    pass