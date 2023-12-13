import machine
import ssd1306

# pycharm IDE may say unused, but these are absolutely required
from i2c_eeprom import i2c_eeprom_init, read_i2c, write_i2c


def init_i2c():
    # I2C Setup Section
    scl_pin = machine.Pin(5)
    sda_pin = machine.Pin(4)
    i2c_zero = machine.I2C(0, scl=scl_pin, sda=sda_pin, freq=400000)
    return i2c_zero


def init_spi_eeprom():
    # SPI Setup Section
    miso = machine.Pin(16, machine.Pin.IN)
    mosi = machine.Pin(19)
    sck = machine.Pin(18)
    scs = machine.Pin(17, machine.Pin.OUT)
    # spi_page = 256
    swp = machine.Pin(20, machine.Pin.OUT)
    swp.high()
    spi_zero = machine.SPI(0, 1_000_000, sck=sck, mosi=mosi, miso=miso, polarity=0, phase=0)
    return spi_zero, scs


def init_oled(i2c_handle):
    oled_WIDTH = 128
    oled_HEIGHT = 64
    oled_addr = 0x3c
    oled = ssd1306.SSD1306_I2C(oled_WIDTH, oled_HEIGHT, i2c_handle, oled_addr)
    return oled
