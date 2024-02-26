import uasyncio as asyncio
import time
from machine import WDT

from library import badge, atomics

if __name__ == '__main__':
    atomics.wdt = WDT(timeout=8388)
    while True:
        asyncio.run(badge.start_main())
        print("Restarting main thread...")
        time.sleep(1)
