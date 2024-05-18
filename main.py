import uasyncio as asyncio
#from machine import WDT

from library import badge, atomics

if __name__ == '__main__':
    #atomics.wdt = WDT(timeout=8388)
    asyncio.run(badge.start_main())
