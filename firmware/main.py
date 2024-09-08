# script for testing badges at the soldering party
# also put ssd1306.py on the badge to be tested
from machine import Pin
from machine import I2C
from neopixel import NeoPixel
from ssd1306 import SSD1306_I2C
print('Howdy world!')
button1 = Pin(1,Pin.IN,Pin.PULL_UP)
button0 = Pin(0,Pin.IN,Pin.PULL_UP)
buttonU = Pin(10,Pin.IN,Pin.PULL_UP)
buttonL = Pin(8,Pin.IN,Pin.PULL_UP)
buttonR = Pin(9,Pin.IN,Pin.PULL_UP)
buttonD = Pin(7,Pin.IN,Pin.PULL_UP)
np_pin = Pin(6)
np = NeoPixel(np_pin,3)
np[0] = np[1] = np[2] = (127,127,127)
np.write()

# i2c = I2C(0,sda=Pin(4), scl=Pin(5),freq=400_000)
# display = SSD1306_I2C(128,64,i2c)
# # cute test of the SSD1306 display
# display.fill(1)
# display.text('BSidesIF Blue', 4, 8, 0)
# display.text('Screen of Death', 4, 20, 0)
# display.rect(70,45,3,3,0,True)
# display.rect(70,51,3,3,0,True)
# display.ellipse(64,48,3,7,0,False,9)
# display.show()

# test the buttonswitches and LEDs, but not forever
while True:
    print(button1.value(), button0.value(), buttonU.value(), buttonL.value(), buttonR.value(), buttonD.value())
    if (button1.value() == 0):   # left button under screen
        np[1] = (0,255,0)        # paint left LED green
    elif (buttonL.value() == 0): # "DPAD" left
        np[1] = (255,255,0)      # paint left led yellow
    else:
        np[1] = (0,0,0)

    if (button0.value() == 0):   # right button under screen
        np[0] = (255,0,0)        # paint middle LED red
    elif (buttonR.value() == 0): # "DPAD" right
        np[0] = (255,0,255)      # paint middle LED magenta
    else:
        np[0] = (0,0,0)

    if (buttonU.value() == 0):   # "DPAD" up
        np[2] = (0,0,255)        # paint right LED blue
    elif (buttonD.value() == 0): # "DPAD" down
        np[2] = (0,255,255)      # paint right LED cyan
    else:
        np[2] = (0,0,0)
    np.write()
