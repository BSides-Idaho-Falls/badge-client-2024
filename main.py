import uasyncio as asyncio
import time
import initialization as fu

i2c_h = fu.init_i2c()
fu.i2c_eeprom_init(i2c_h)
oled_h = fu.init_oled(i2c_h)






async def start_main():
    pass


if __name__ == '__main__':
    while True:
        asyncio.run(start_main())
        print("Restarting main thread...")
        time.sleep(1)

