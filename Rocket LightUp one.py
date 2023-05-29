import time, gc, os
import adafruit_dotstar
import board, analogio
import feathers2

# Make sure the 2nd LDO is turned on
feathers2.enable_LDO2(True)

# Create a DotStar instance
dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=3.5, auto_write=True)
dotstar2 = adafruit_dotstar.DotStar(board.D9,board.D6,1, brightness=2.5)
dotstar3 = adafruit_dotstar.DotStar(board.D9,board.D6,1, brightness=2.5)
# Create a reference to the ambient light sensor so we can read it's value
light = analogio.AnalogIn(board.AMB)

# Say hello
print("\nHello from FeatherS2!")
print("---------------------\n")

# Turn on the internal blue LED
feathers2.led_set(True)

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))

flash = os.statvfs('/')
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
# Show flash size
print("Flash - os.statvfs('/')")
print("---------------------------")
print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))

print("Dotstar Time!\n")

# Create a colour wheel index int
color_index = 0
color_index2 = 0
color_index3 = 0

# Rainbow colours on the Dotstar
while True:
    # Get the R,G,B values of the next colour
    r,g,b = feathers2.dotstar_color_wheel( color_index )
    r2,g2,b2 = feathers2.dotstar_color_wheel( color_index2 )
    r3,g3,b3 = feathers2.dotstar_color_wheel( color_index3 )

    # Set the colour on the dotstar
    dotstar[0] = ( r, g, b, 0.5)
    dotstar2[0] = (r2, g2, b2, 0.5)
    dotstar3[0] = (r3, g3, b3, 0.5)
    # Increase the wheel index
    color_index += 10
    color_index2 += 10
    color_index3 += 10

    # If the index == 255, loop it
    if color_index == 255:
        color_index = 0
        # Invert the internal LED state every half colour cycle
        feathers2.led_blink()
        # Print the ambient light value
        # This is a number translated fom a voltage via the ADC (Analog to Digital Converter)
        print("Ambient Light Reading: {}".format(light.value))
    if color_index2 == 255:
        color_index2 = 0
    if color_index3 == 255:
        color_index3 = 0

    # Sleep for 15ms so the colour cycle isn't too fast
    time.sleep(0.150)